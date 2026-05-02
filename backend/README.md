# Ask-Prof-Fan QA Backend

FastAPI service that answers questions about Prof. Yao-Chung Fan, grounded
in the markdown files served from `yfan.nlpnchu.org`. Uses Claude with
prompt caching, streams responses back via SSE. Designed to run on
Google Cloud Run.

## Architecture

```
[browser chat input on yfan.nlpnchu.org]
            ↓ POST /chat {q}
   [Cloud Run: this FastAPI service]
            ↓ Claude messages.stream()
       [Anthropic API]
            ↓ tokens
        SSE stream back to browser
```

On startup the service fetches:

- `https://yfan.nlpnchu.org/llms.txt`
- `https://yfan.nlpnchu.org/about.md`
- `https://yfan.nlpnchu.org/publications.md`
- `https://yfan.nlpnchu.org/services.md`

…and bakes them into a single cached system prompt. Total ≈ a few KB; well
under the cache threshold for Sonnet, so caching may be a no-op for the
first iteration — keep the directive anyway, it's free if it doesn't help.

To refresh the context after editing markdown, redeploy the service.

## Endpoints

- `GET  /healthz` → `{ok, model, context_chars, rate_limit}`
- `POST /chat`    → SSE stream. Body: `{"q": "..."}` (max 500 chars).
  Each event: `data: {"t": "..."}` for text chunks, `data: [DONE]` at end,
  `data: {"error": "..."}` on failure.

## Local dev

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
uvicorn main:app --reload --port 8080
# test:
curl -N http://localhost:8080/chat -H 'Content-Type: application/json' \
  -d '{"q":"范老師最近發表的論文有哪些？"}'
```

## Deploy to Cloud Run

One-time setup:

```bash
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
                       secretmanager.googleapis.com

# Store the Anthropic key in Secret Manager
echo -n "sk-ant-..." | gcloud secrets create anthropic-api-key \
  --data-file=- --replication-policy=automatic
```

Deploy (re-run for any update):

```bash
cd backend
gcloud run deploy yfan-qa \
  --source . \
  --region asia-east1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi --cpu 1 \
  --concurrency 20 \
  --min-instances 0 --max-instances 5 \
  --timeout 60s \
  --set-env-vars CLAUDE_MODEL=claude-sonnet-4-6,MAX_TOKENS=600 \
  --set-secrets ANTHROPIC_API_KEY=anthropic-api-key:latest
```

Cloud Run will print the URL, e.g. `https://yfan-qa-xxxxx-de.a.run.app`.

### Custom domain (optional)

Map `qa.yfan.nlpnchu.org` to the service:

```bash
gcloud beta run domain-mappings create \
  --service yfan-qa --domain qa.yfan.nlpnchu.org --region asia-east1
```

Then add the CNAME shown by gcloud to your DNS (Cloudflare for nlpnchu.org).

If you skip the custom domain, the frontend just points at the
`*.run.app` URL — CORS already allows it via the wildcard origin handling.

## Model & cost notes

- Default model is `claude-sonnet-4-6`. For cheaper / faster, switch the
  env var to `claude-haiku-4-5`.
- A typical Q&A turn here is ~3–4 KB system prompt + short user question
  + ~200 tokens out. Pricing is publicly listed at anthropic.com/pricing —
  on Sonnet 4.6 expect well under USD $0.01 per question.
- Rate limiting is 10 questions per IP per 60s, in-memory, naive but
  enough to deter casual abuse on a personal site. Tune via env vars.

## Wiring the frontend

In the homepage chat handler, set the API base:

```javascript
const API_URL = 'https://yfan-qa-xxxxx-de.a.run.app/chat';
// or after custom domain mapping:
// const API_URL = 'https://qa.yfan.nlpnchu.org/chat';
```

The `prototype/v-warm/index.html` chat handler is already wired for SSE;
just paste the URL.

## Things this service deliberately does NOT do

- No vector store / RAG — content is small enough to fit in context.
- No DB. No auth. No conversation memory between requests.
- No request logging beyond stderr (Cloud Run captures stdout/stderr).
  Add structured logging later if traffic warrants.
