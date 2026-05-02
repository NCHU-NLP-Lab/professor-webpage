"""
Ask-Prof-Fan QA backend — FastAPI on Cloud Run.

Flow:
  1. On startup, fetch the 4 markdown files from yfan.nlpnchu.org
     (llms.txt, about.md, publications.md, services.md) — total a few KB.
  2. POST /chat receives a question, asks Claude with the markdown as a
     cached system prompt, streams tokens back via SSE.
  3. Naive in-memory rate-limit per IP.
"""

from __future__ import annotations

import json
import logging
import os
from collections import deque
from contextlib import asynccontextmanager
from time import monotonic
from typing import AsyncIterator

import httpx
from anthropic import AsyncAnthropic
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("yfan-qa")

ALLOWED_ORIGINS = [
    "https://yfan.nlpnchu.org",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CONTEXT_URLS = [
    "https://yfan.nlpnchu.org/llms.txt",
    "https://yfan.nlpnchu.org/about.md",
    "https://yfan.nlpnchu.org/publications.md",
    "https://yfan.nlpnchu.org/services.md",
]

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "600"))
RL_LIMIT = int(os.getenv("RATE_LIMIT", "10"))      # per IP per window
RL_WINDOW = int(os.getenv("RATE_WINDOW", "60"))    # seconds

SYSTEM_PROMPT_TEMPLATE = """You answer questions about Prof. Yao-Chung Fan (范耀中) on his personal homepage at yfan.nlpnchu.org. You are NOT his AI assistant — you are an information desk on his website.

Rules:
- Answer ONLY from the SOURCE MATERIAL below. Do not use outside knowledge.
- Match the language of the question (中文問 → 中文答；English → English).
- Be concise: 1–3 short paragraphs. No filler. No marketing tone.
- If the answer is not in the source, say so honestly. Suggest where to look:
    NLP Lab homepage: https://nlpnchu.org
    eduxplore (campus AI advisor): https://eduxplore.nlpnchu.org
    Google Scholar / DBLP / ORCID (links on the homepage)
- Do NOT speculate about Prof. Fan's opinions, character, personal life, or
  unstated future plans.
- Do NOT invent papers, services, or affiliations not present in the source.
- For questions about Prof. Fan's email or contact: yfan@nchu.edu.tw, Science Building Room 704, NCHU.

==== SOURCE MATERIAL ====
{context}
==== END OF SOURCE MATERIAL ===="""


# ---- context loading ------------------------------------------------------

_context_text: str = ""
_system_prompt: str = ""


async def _fetch_context() -> str:
    parts: list[str] = []
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        for url in CONTEXT_URLS:
            try:
                r = await client.get(url)
                r.raise_for_status()
                fname = url.rsplit("/", 1)[-1]
                parts.append(f"## {fname}\n\n{r.text.strip()}")
                log.info("fetched %s (%d bytes)", url, len(r.text))
            except Exception as e:
                log.warning("failed to fetch %s: %s", url, e)
                parts.append(f"## {url} — fetch failed")
    return "\n\n---\n\n".join(parts)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    global _context_text, _system_prompt
    _context_text = await _fetch_context()
    _system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=_context_text)
    log.info(
        "boot: model=%s, context=%d chars, system_prompt=%d chars",
        MODEL, len(_context_text), len(_system_prompt),
    )
    yield


# ---- app ------------------------------------------------------------------

app = FastAPI(title="Ask Prof Fan", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type"],
    max_age=86400,
)

client = AsyncAnthropic()  # reads ANTHROPIC_API_KEY


# ---- naive rate limiting --------------------------------------------------

_rl: dict[str, deque] = {}


def _rate_check(ip: str) -> bool:
    now = monotonic()
    dq = _rl.setdefault(ip, deque())
    while dq and dq[0] < now - RL_WINDOW:
        dq.popleft()
    if len(dq) >= RL_LIMIT:
        return False
    dq.append(now)
    return True


def _client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for", "")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


# ---- routes ---------------------------------------------------------------

class ChatReq(BaseModel):
    q: str = Field(min_length=1, max_length=500)


@app.get("/healthz")
async def healthz():
    return {
        "ok": True,
        "model": MODEL,
        "context_chars": len(_context_text),
        "rate_limit": f"{RL_LIMIT}/{RL_WINDOW}s",
    }


@app.post("/chat")
async def chat(body: ChatReq, request: Request) -> StreamingResponse:
    ip = _client_ip(request)
    if not _rate_check(ip):
        raise HTTPException(status_code=429, detail="rate limit exceeded")

    async def stream() -> AsyncIterator[str]:
        try:
            async with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=[
                    {
                        "type": "text",
                        "text": _system_prompt,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                messages=[{"role": "user", "content": body.q}],
            ) as st:
                async for chunk in st.text_stream:
                    yield f"data: {json.dumps({'t': chunk}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            log.exception("chat error")
            yield f"data: {json.dumps({'error': str(e)[:200]}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
