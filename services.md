# Deployed AI Services — NCHU NLP Lab (Yao-Chung Fan, Director)

The NCHU NLP Lab operates a family of AI systems spanning campus services, smart agriculture, library and museum applications, healthcare, and Indigenous-language preservation.

## Campus and Language

### AI 興學伴 (eduxplore)

Campus learning advisor integrating NCHU's institutional information (course search, faculty lookup, learning resources) into a conversational interface.

- URL: https://eduxplore.nlpnchu.org/
- Tech / keywords: LLM, RAG, Campus Integration
- Status: **Live**

### Fact-Checking System — 事實查核系統

End-to-end fact verification system using Claude API and the Model Context Protocol (MCP) to coordinate retrieval, evidence checking, and verdict generation.

- Tech / keywords: Claude API, MCP, Agent
- Status: **Live**

### Amis (阿美族語) Dialogue System — 阿美族語對話系統

LLM + speech recognition system for Amis, a low-resource Indigenous Taiwanese language, supporting language preservation, education, and accessibility.

- Tech / keywords: LLM, ASR, Indigenous Lang., Low-Resource
- Status: **Research / Deployed**

## Smart Agriculture

### 神農 Agent (Demeter)

AI plant doctor built with NCHU's Smart Sustainable New Agriculture Research Center: an LLM agent with 72 domain tools for pest and disease diagnosis, registered-pesticide recommendation, and academic resource search.

- URL: https://demeter.nlpnchu.org/
- Tech / keywords: Agent, Tool Use, Plant Diagnosis
- Status: **Live**

### Grape & Beefsteak Tomato Agricultural Knowledge Graph — 農業知識圖譜

Interactive agricultural knowledge graph for grape and beefsteak tomato, used as the reasoning backbone for the diagnosis and greenhouse-patrol systems.

- URL: https://kg.nlpnchu.org/
- Tech / keywords: Knowledge Graph, Agriculture
- Status: **Live**

### Smart Greenhouse Patrol — 智慧溫室巡檢

An AI-driven greenhouse patrol vehicle that navigates by cameras alone, measures on site, consults the knowledge graph, and raises warnings before disease symptoms appear.

- URL: https://robot.nlpnchu.org/
- Tech / keywords: Embodied Agent, VLM, Knowledge Graph
- Status: **Research**

### Animal Infectious Disease Prioritization System — 動物傳染病優先排序系統

Experimental research prototype for prioritizing animal infectious diseases (not an official result; research reference only).

- Tech / keywords: Decision Support, Prototype
- Status: **Prototype**

## Library and Culture

### AI 小貓 (AI-assisted Cataloging)

AI-assisted cataloging for the NCHU Library: matches NCL CIP, Library of Congress authority records, and similar local holdings to propose traceable classification and call-number suggestions, with librarians making the final decision.

- URL: https://aicat.nlpnchu.org/
- Tech / keywords: Cataloging, Retrieval, Human-in-the-loop
- Status: **Trial**

### Giant Unearthed (鯨掘・骨語) WebAR Exhibit — 鯨掘・骨語 WebAR

Interactive missions and a WebAR experience for the joint exhibition by the NCHU Library, the National Museum of Natural Science, and the NCHU Museum of Natural History.

- URL: https://whale.nlpnchu.org/
- Tech / keywords: WebAR, Exhibit, Interactive
- Status: **Live**

### VisionBridge

Multisensory visual description platform: curators use vision-language models to generate audio descriptions of artworks, conditioned on the intended listener.

- URL: https://visionbridge.nlpnchu.org/
- Tech / keywords: VLM, Accessibility, Audio Description
- Status: **Live**

## Healthcare

### MedScribe — MedScribe AI 聽診助手

Ambient clinical scribe: transcribes doctor-patient conversations in real time, organizes a structured history following OPQRST-A, and alerts the physician to red-flag symptoms.

- URL: https://asr.nlpnchu.org/
- Tech / keywords: ASR, LLM, Clinical Notes
- Status: **Research / Demo**

## Past Projects

For earlier projects (神農 TAIDE — RAG on the TAIDE LLM, Querator AI for question generation, etc.), see the personal site at https://yfan.nlpnchu.org/.
