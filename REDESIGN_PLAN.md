# 個人首頁改版規劃 — Yao-Chung Fan

> 工作中的規劃文件。會隨討論持續更新，最後實作完成後可移除。

## 一、現況體檢

目前 `index.html` 是 2013 年那一代的 Bootstrap + jQuery One-Page 模板（SquareRoot）：
preloader gif、`jquery-1.10.2`、Owl Carousel、文字旋轉外掛、舊式時間軸動畫。

**根本問題**：一個做 NLP / NLG / LLM 的教授，網頁本身卻沒有任何「生成」、任何
「智慧」的成分；內容停留在 2018 前後的舊專案（Querator AI、法院判決書、
結核病檢測…），完全沒有反映目前的研究與服務部署現況。

要從這裡跳到「不同等級」，方向不是「換一個更潮的 template」，而是讓首頁本身
成為研究的展示場 (research-as-medium)。

## 二、核心理念

> **首頁不是被「載入」，而是被「生成」。**

- 視覺第一秒就讓訪客感受到「這個網站本身是 NLP 系統的輸出」。
- 把現有部署中的 AI 服務家族（AI 興學伴 / 神農 TAIDE / 事實查核 /
  彰基諮詢 / 阿美族語對話系統）放到首頁主秀位置，證明
  「研究 → 產品 → 服務全校 → 跨機構落地」這條完整鏈路。
- **副教務長**（教務行政）+ 教授（研究）+ NLP Lab 主持人（產品落地）三軌
  身份要被看到，不是只有「教授」一個 label。

## 三、Hero 概念（已演進）

第一版構想：用 Querator AI 當 Live Demo 主秀。
**修正**：Querator 是 2018–2022 的成果，已舊。改以 **AI 興學伴
（eduxplore.nlpnchu.org）** 為主秀。

新版 Hero 構想：
- 黑底、等寬字、極簡。
- 名字、頭銜、研究方向以 token streaming 動畫逐字浮現
  （節奏模擬真實 LLM 輸出：variable delay、偶爾 backspace 修正）。
- 背景：Canvas / WebGL 的 token embedding 粒子流（節點 + 連線、緩慢漂移）。
- 畫面正中放一個 **聊天輸入框**，placeholder：「Ask me about Professor Fan」。
  訪客打字 → 後端（如可開放：eduxplore API）→ 即時回答關於范老師的研究、
  課程、論文。等於把最酷的產品當成名片。

## 四、區段規劃

| Section | 目的 | 「酷」的具體做法 |
|---|---|---|
| **Hero** | 第一秒建立差異化 | Token streaming 動畫 + 聊天輸入框（接 AI 興學伴） |
| **Identity** | 三軌身份 | 教授 / **副教務長** / NLP Lab 主持人，並列呈現 |
| **Live Demo: AI 興學伴** | 展示已部署中的服務 | 嵌入或連結 eduxplore.nlpnchu.org，附上使用量數字（待補） |
| **Deployed Services** | 證明「能做出來、能落地」 | 卡片陣列：神農 TAIDE / 事實查核（Claude API + MCP）/ 彰基諮詢 / 阿美族語對話系統，每張附簡短規格與一段 demo |
| **Research Constellation** | 視覺化學術版圖 | d3-force 力導向圖，節點 = paper，顏色 = topic（NLG / MRC / Continual Learning / Agentic AI / 原住民族語…），可拖曳、hover、click 開 PDF |
| **Impact** | 真實學術影響力 | h-index、引用數、頂會數，scroll 觸發 count-up + sparkline，從 Google Scholar 拉真實資料 |
| **Recent Work** | 2024–2026 主軸 | Agentic AI、阿美語對話系統、教育科技 LLM…（待范老師補充清單） |
| **Lab & Students** | 學生作品與招生 | 乾淨 grid 取代現在的 YouTube iframe 牆 |
| **Timeline / CV** | 學經歷 | 留下，重做動畫與排版 |
| **Footer** | 聯絡 | Email、Office、Lab 連結 |

舊專案（Querator、法院判決書、結核病、用電熱點圖、TELENOTE…）降為附錄
或「Past Projects」摺疊清單，不再佔主要視線。

## 五、技術路線

保持靜態，跑在 GitHub Pages（`yfan.nlpnchu.org`）上。

- 純 HTML5 + 現代 CSS（custom properties、container queries、OKLCH、
  `view-timeline` scroll-driven animations）+ 原生 ES Modules。
- 拋棄 jQuery / Bootstrap / Owl / preloader 全家桶。
- d3 只引需要的模組；Hero 背景 Canvas 自寫。
- 變體字：JetBrains Mono + Inter（或 Geist）。
- 視覺語言：全黑底 + 單一強調色（OKLCH 綠或青），留白大、層級深。
  座標：Vercel / Linear / Anthropic 官網質感，但更冷、更 lab。
- Lighthouse 100/100；首屏 gzip 後 < 50KB。
- 尊重 `prefers-reduced-motion`、鍵盤可達、語意 HTML、色彩對比 AA+。

## 六、服務家族（依 nlpnchu.org 與 eduxplore.nlpnchu.org 公開資訊）

> 2026-05-01 web search 抓到的清單。實際細節仍待范老師補正。

| 服務 | 對象 | 已知技術線索 | 狀態 |
|---|---|---|---|
| **AI 興學伴 / eduxplore** | 中興大學師生 | 整合校務資訊（課程搜尋、師資查詢…），定位為 LearningHub | 已上線 `eduxplore.nlpnchu.org` |
| **神農 TAIDE** | 農業 / 校內？ | 基於台灣本土 LLM (TAIDE) 的 RAG 架構 | 已上線 |
| **事實查核系統** | 一般使用者 / 媒體 | Claude API + MCP 協議 | 已上線 |
| **彰化基督教醫院諮詢系統** | 醫院訪客 / 員工 | 入館規則智慧問答 | 已上線（跨機構落地的代表作） |
| **阿美族語對話系統** | 原住民語使用者 / 教學 | LLM + 語音辨識，低資源語言應用 | 研究/部署中 |

~~**SDG Explore**~~ 已不在服務名單（2026-05-01 范老師確認）。

## 七、待范老師確認的事項

1. **服務名稱正名**：是「AI **興**學伴」還是「AI **新**學伴」？官方域名是
   `eduxplore`，看起來「興」是正式名（諧音「興大 + 興學」）。
2. **SDG Explore 還在嗎？** 還是已併入興學伴？
3. **底層架構分工**：上表中興學伴 / 神農 / 彰基諮詢分別走自家模型還是 API？
   決定首頁能不能標榜「自研」或「整合」或「兼具」。
4. **使用量數字**：可不可以公開「已服務 X 名學生 / 回答 Y 個問題 /
   涵蓋 Z 門課程」？特別是彰基那條，跨機構的數字最有說服力。
5. ~~**Demo 後端可用性**~~：**已決議：先做 UI 殼層（canned demo），eduxplore
   後端後續再串接。** 殼層仍要做出 token streaming 的真實感，讓氣質先到位。
6. **行政身份露出**：**副教務長**這個身份是現任嗎？要不要在 Identity 主露出？
   （建議：要 — 教務長層級的行政 + AI 落地全校，是非常硬的差異化訊號。）
7. **Recent Work 主軸**：Agentic AI、阿美族語、教育科技 LLM、表格檢索（ACL 2025）…
   想列哪幾個？
8. **語言策略**：中文為主英文為輔？還是英文為主給國際同行看？

## 八、執行進路

兩個選項：
- **(A) 一次到位**：直接重寫整站，先做 Hero + 興學伴 Demo + Constellation 三段，
  其他沿用文字內容但重排。
- **(B) 先做 Hero 原型**：只做 Hero 一段給范老師看，氣質對了再展開全站。

**目前傾向 (B) → (A)**：避免做完才發現方向不對。

## 九、現階段進度

- [x] 現況體檢
- [x] 核心理念與視覺方向
- [x] Hero 概念（已演進到以 AI 興學伴為主秀）
- [x] 全站區段規劃（草稿）
- [x] 技術路線決策
- [x] 服務家族公開資訊收集（2026-05-01 web search）
- [x] 副教務長身份納入 Identity 規劃
- [x] SDG Explore 確認移除
- [x] Hero 聊天框策略確定：先做 UI 殼層
- [x] Hero 原型實作（`prototype/hero.html`）
- [x] 三變體迭代（v-glow / v-warm / v-light），最終選定 **v-warm**
- [x] QA 後端實作 + 部署 Cloud Run（`backend/`，2026-05-02 上線於 asia-east1）
- [x] 全站實作 — v-warm 變體於 2026-05-02 升為正式版根 `index.html`，
      舊 SquareRoot 模板 / 老 asset / `prototype/` 目錄全數清除
- [ ] 范老師回覆第七節剩餘待確認事項（不影響上線；之後依回覆微調文案 / 服務名 / 行政身份露出）
