# professor-webpage

教授個人網頁 — Yao-Chung Fan / 范耀中
National Chung Hsing University, Department of Computer Science

正式網址：https://yfan.nlpnchu.org/

## 架構

- 靜態前端：根目錄 `index.html`，跑在 GitHub Pages 上（CNAME → `yfan.nlpnchu.org`）。
  純 HTML / CSS / 原生 JS，無建置流程，編輯完直接 push。
- QA 後端：`backend/` 內 FastAPI 服務，部署在 Google Cloud Run。
  Hero 區的聊天框會打 `/chat`，由 Claude 以本站的 `*.md` / `llms.txt` 為
  source 串流回答（SSE）。詳見 `backend/README.md`。
- LLMO（給 LLM 爬蟲讀的）：`llms.txt` + `about.md` / `publications.md` /
  `services.md` + `robots.txt` + `sitemap.xml`。內容更新時記得同步這幾份
  並重新 deploy backend，讓 QA 抓到最新版本。

## 改版歷史

舊版（2013 SquareRoot Bootstrap+jQuery 模板）已於 2026-05 全面替換成
編輯式新版（v-warm 變體）。改版思路與規劃見 `REDESIGN_PLAN.md`。
