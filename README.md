<div align="center">

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Bebas+Neue&size=60&duration=3000&pause=1000&color=E8FF47&center=true&vCenter=true&width=600&lines=SUMMARAI+V2;FULL+AI+MODE;TEXT+INTELLIGENCE" alt="SummarAI V2"/>

<br/>

# ◈ SummarAI V2
### The Full AI-Powered Text Summarization Engine

<p align="center">
  <em>Paste text. Upload a PDF. Drop a URL.</em><br/>
  <em>Get a sharp, accurate summary in seconds — full BART transformer, zero restrictions.</em>
</p>

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-BART--Large--CNN-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/facebook/bart-large-cnn)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.2-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-8B5CF6?style=for-the-badge)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-E8FF47?style=for-the-badge)](https://github.com/TUSHARTAMRAKAR/Text-Summarizer-Tool-V2/pulls)

<br/>

```
╔══════════════════════════════════════════════════════════════╗
║   ◈ SummarAI V2    |  Full BART  |  PDF  |  URL  |  Export  ║
╠═══════════════════════╦══════════╦═══════════════════════════╣
║                       ║          ║                           ║
║   01  INPUT           ║  [SUM-]  ║   02  SUMMARY            ║
║                       ║  [MAR-]  ║                           ║
║   ✏️ Text / 📄 PDF    ║  [IZE ]  ║   Concise. Accurate.     ║
║   🔗 URL              ║   ⟶     ║   Instant.               ║
║                       ║          ║                           ║
╠═══════════════════════╩══════════╩═══════════════════════════╣
║  Original: 500w  │  Summary: 82w  │  Compression: 84%        ║
╚══════════════════════════════════════════════════════════════╝
```

<br/>

### 🔗 Quick Links

[📦 V1 — Hosted Version](https://github.com/TUSHARTAMRAKAR/Text-Summarizer-Tool) &nbsp;·&nbsp;
[🌐 Live Demo (V1)](https://summari-84uc.onrender.com) &nbsp;·&nbsp;
[📖 API Reference](docs/API.md) &nbsp;·&nbsp;
[🐛 Report Bug](https://github.com/TUSHARTAMRAKAR/Text-Summarizer-Tool-V2/issues) &nbsp;·&nbsp;
[✨ Request Feature](https://github.com/TUSHARTAMRAKAR/Text-Summarizer-Tool-V2/issues)

<br/>

> ⚠️ **V2 is a local-first application.** It runs the full `facebook/bart-large-cnn` model (~1.6GB)
> which requires ~2GB RAM — beyond free cloud hosting limits.
> For the hosted version, see **[SummarAI V1 →](https://github.com/TUSHARTAMRAKAR/Text-Summarizer-Tool)**

</div>

---

## 📌 Table of Contents

- [V1 vs V2](#-v1-vs-v2--whats-different)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [How It Works](#-how-it-works)
- [API Reference](#-api-reference)
- [Running Tests](#-running-tests)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## ⚔️ V1 vs V2 — What's Different?

| | V1 — Hosted | V2 — Local (this repo) |
|---|---|---|
| 🌐 **Deployment** | Live on Render (free tier) | Run locally on your machine |
| 🧠 **Abstractive (BART)** | ❌ Disabled — RAM limit | ✅ Fully unlocked |
| ✂️ **Extractive (TF-IDF)** | ✅ | ✅ |
| 📎 **PDF Upload** | ❌ | ✅ |
| 🔗 **URL Summarizer** | ❌ | ✅ |
| 📤 **Export (.txt / .pdf)** | ❌ | ✅ |
| 🌙 **Dark / Light Mode** | ❌ | ✅ |
| 📜 **Summary History** | ❌ | ✅ (last 10) |
| 💾 **RAM Required** | < 512MB | ~2GB |
| ⚡ **Summary Quality** | Good | Best |

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🧠 Full Abstractive Summarization
Uses `facebook/bart-large-cnn` — the same transformer architecture powering production AI systems. Reads, understands, and **rewrites** your text in its own words.

</td>
<td width="50%">

### ✂️ Extractive Summarization
Custom TF-IDF scoring engine — ranks every sentence by statistical importance and returns the most critical ones. Fast, deterministic, zero model required.

</td>
</tr>
<tr>
<td>

### 📎 PDF Upload & Extraction
Drag and drop any PDF. PyMuPDF extracts the full text, feeds it through the NLP engine, and returns a clean summary — even for long research papers.

</td>
<td>

### 🔗 URL Article Scraper
Paste any article link. BeautifulSoup fetches and parses the page, strips ads/nav/footers, extracts pure content, and summarizes it instantly.

</td>
</tr>
<tr>
<td>

### 📤 Export Summary
Download your summary as a formatted `.txt` file or a clean `.pdf` document — complete with metadata, word counts, and compression stats.

</td>
<td>

### 📜 Summary History
Every summary is automatically saved in a session history panel. Click any past entry to restore it instantly. Stores your last 10 summaries.

</td>
</tr>
<tr>
<td>

### 🌙 Dark / Light Mode
Full theme system with smooth transitions. Preference is saved in localStorage — your chosen theme persists across sessions.

</td>
<td>

### 📏 3 Summary Lengths
Short (30–80 tokens), Medium (80–180 tokens), Long (180–350 tokens). Full control over how much detail you want in the output.

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Frontend** | HTML5, CSS3, Vanilla JS | — | UI, interactions, API calls |
| **Backend** | Python, Flask | 3.10+, 3.0 | REST API server |
| **AI Model** | HuggingFace Transformers | 4.35.2 | Abstractive summarization |
| **Deep Learning** | PyTorch | 2.2.0 | Model inference engine |
| **PDF Parsing** | PyMuPDF (fitz) | 1.23.8 | PDF text extraction & export |
| **Web Scraping** | BeautifulSoup4 + Requests | 4.12.3 | URL article extraction |
| **NLP Algorithm** | Custom TF-IDF | — | Extractive summarization |
| **Testing** | pytest | 7.4.0 | Unit + integration tests |

---

## 🗂️ Project Structure

```
Text-Summarizer-Tool-V2/
│
├── 📂 backend/
│   ├── app.py                  # Flask application — all API routes
│   │                           # Endpoints: /api/summarize, /api/summarize-pdf,
│   │                           #            /api/summarize-url, /api/export, /api/health
│   └── summarizer.py           # Core NLP engine
│                               # — BART abstractive pipeline
│                               # — Custom TF-IDF extractive algorithm
│
├── 📂 frontend/
│   ├── templates/
│   │   └── index.html          # Single-page app UI
│   │                           # — Text / PDF / URL input modes
│   │                           # — Dark / Light theme toggle
│   │                           # — Summary history panel
│   └── static/
│       ├── css/
│       │   └── style.css       # Full design system
│       │                       # — CSS variables for theming
│       │                       # — Animated hero, glowing nav pills
│       │                       # — Responsive layout
│       └── js/
│           └── main.js         # All frontend logic
│                               # — Source switching (text/pdf/url)
│                               # — API calls, state management
│                               # — Export, copy, history
│
├── 📂 tests/
│   └── test_summarizer.py      # 15 unit + integration tests
│
├── 📂 docs/
│   └── API.md                  # Full API endpoint reference
│
├── requirements.txt            # Pinned Python dependencies
├── .gitignore                  # Excludes venv, cache, model files
├── LICENSE                     # MIT License
└── README.md                   # This file
```

---

## 🚀 Getting Started

### System Requirements

| Requirement | Specification |
|---|---|
| **OS** | Windows 10+, macOS 12+, Ubuntu 20.04+ |
| **Python** | 3.10 or higher |
| **RAM** | 4GB recommended (2GB minimum) |
| **Disk** | ~3GB free (model cache + dependencies) |
| **Internet** | Required on first run (model download ~1.6GB) |

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/TUSHARTAMRAKAR/Text-Summarizer-Tool-V2.git
cd Text-Summarizer-Tool-V2
```

### Step 2 — Create Virtual Environment

```bash
python -m venv venv
```

### Step 3 — Activate Virtual Environment

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

You'll see `(venv)` at the start of your terminal. ✅

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

> ⏳ First run downloads `facebook/bart-large-cnn` (~1.6GB). Cached locally after that.

### Step 5 — Run the Application

```bash
cd backend
python app.py
```

### Step 6 — Open in Browser

```
http://localhost:5000
```

**🎉 You're live.**

---

## 🧠 How It Works

### Abstractive Summarization — BART Transformer

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR INPUT TEXT                      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   BART ENCODER                          │
│  Reads every token, builds bidirectional understanding  │
│  of context, relationships, and key information         │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   BART DECODER                          │
│  Auto-regressively generates summary token by token     │
│  Beam search finds the highest-probability sequence     │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              FRESH HUMAN-LIKE SUMMARY                   │
│  Completely new sentences — not copied from original    │
└─────────────────────────────────────────────────────────┘
```

**Model:** `facebook/bart-large-cnn` — fine-tuned by Meta AI on 300,000+ CNN/DailyMail article-summary pairs. Learned to compress information exactly the way a journalist would.

---

### Extractive Summarization — TF-IDF Scoring

```
Input Text
    │
    ├─▶ Split into sentences
    │
    ├─▶ Build word frequency table
    │       TF  = word frequency in sentence
    │       IDF = rarity across full document
    │       Score = TF × IDF (normalized)
    │
    ├─▶ Score each sentence
    │       sentence_score = Σ word_scores
    │       + position boost for early sentences
    │
    └─▶ Return top N sentences in original order
```

Zero external NLP libraries. Pure Python math. Instant, deterministic, fully offline.

---

### PDF Pipeline

```
PDF File → PyMuPDF → Raw Text Extraction → NLP Engine → Summary
```

### URL Pipeline

```
URL → requests.get() → BeautifulSoup → Strip nav/ads/footer
    → Extract <p> tags → Clean whitespace → NLP Engine → Summary
```

---

## 🔌 API Reference

Full documentation → [`docs/API.md`](docs/API.md)

**Base URL:** `http://localhost:5000`

---

### `POST /api/summarize` — Summarize Text

```bash
curl -X POST http://localhost:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your article...", "length": "medium", "method": "abstractive"}'
```

| Parameter | Type | Options | Default |
|---|---|---|---|
| `text` | string | 50–50,000 chars | required |
| `length` | string | `short` · `medium` · `long` | `medium` |
| `method` | string | `abstractive` · `extractive` | `abstractive` |

**Response:**
```json
{
  "success": true,
  "summary": "AI is reshaping industries at unprecedented scale...",
  "original_word_count": 500,
  "summary_word_count": 82,
  "compression_ratio": "84%",
  "method_used": "abstractive"
}
```

---

### `POST /api/summarize-pdf` — Summarize PDF

```bash
curl -X POST http://localhost:5000/api/summarize-pdf \
  -F "file=@document.pdf" \
  -F "length=medium" \
  -F "method=abstractive"
```

---

### `POST /api/summarize-url` — Summarize URL

```bash
curl -X POST http://localhost:5000/api/summarize-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article", "length": "medium", "method": "abstractive"}'
```

---

### `POST /api/export` — Export Summary

```bash
curl -X POST http://localhost:5000/api/export \
  -H "Content-Type: application/json" \
  -d '{"summary": "...", "format": "pdf", "method_used": "abstractive"}' \
  --output summary.pdf
```

---

### `GET /api/health` — Health Check

```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "2.0.0",
  "features": ["text", "pdf", "url", "export"]
}
```

---

## 🧪 Running Tests

```bash
# From project root with venv active
python -m pytest tests/ -v
```

```
tests/test_summarizer.py::TestExtractive::test_extractive_returns_dict     PASSED ✅
tests/test_summarizer.py::TestExtractive::test_extractive_success_flag     PASSED ✅
tests/test_summarizer.py::TestExtractive::test_extractive_has_summary      PASSED ✅
tests/test_summarizer.py::TestExtractive::test_extractive_method_label     PASSED ✅
tests/test_summarizer.py::TestExtractive::test_extractive_word_counts      PASSED ✅
tests/test_summarizer.py::TestWordCounting::test_compression_ratio         PASSED ✅
tests/test_summarizer.py::TestEdgeCases::test_handles_multiline_text       PASSED ✅
tests/test_summarizer.py::TestEdgeCases::test_all_length_options           PASSED ✅
tests/test_summarizer.py::TestAPIEndpoints::test_health_endpoint           PASSED ✅
tests/test_summarizer.py::TestAPIEndpoints::test_summarize_endpoint_valid  PASSED ✅
──────────────────────────────────────────────────────────────────────────────────
15 passed in 3.42s
```

---

## 🗺️ Roadmap

```
v2.0.0  ✅ Released
        ├── Full BART abstractive summarization
        ├── TF-IDF extractive summarization
        ├── PDF upload & extraction
        ├── URL article scraper
        ├── Export as .txt and .pdf
        ├── Dark / Light mode
        ├── Summary history (last 10)
        └── Full REST API

v2.1.0  🔲 Planned
        ├── Keyword extraction (top 5 terms)
        ├── Sentiment analysis (positive / negative / neutral)
        └── Reading time estimator

v2.2.0  🔲 Planned
        ├── SQLite database — permanent summary storage
        ├── Multi-language summarization
        └── Side-by-side abstractive vs extractive comparison

v3.0.0  🔲 Future
        ├── User authentication system
        ├── Docker containerization
        ├── CI/CD pipeline (GitHub Actions)
        └── GPU acceleration support
```

---

## 🤝 Contributing

Contributions are what make open source incredible. Any contribution you make is **genuinely appreciated**.

### How to Contribute

```bash
# 1. Fork the repo
# 2. Create your feature branch
git checkout -b feature/AmazingFeature

# 3. Commit your changes (use Conventional Commits)
git commit -m "feat: add keyword extraction to summary output"

# 4. Push to your branch
git push origin feature/AmazingFeature

# 5. Open a Pull Request
```

### Commit Message Convention

| Prefix | Use for |
|---|---|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation changes |
| `style:` | CSS / formatting changes |
| `refactor:` | Code restructuring |
| `test:` | Adding tests |
| `chore:` | Build / config changes |

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for full details.

You are free to use, copy, modify, merge, publish, distribute, sublicense, and sell copies — as long as the original license notice is included.

---

## 🙏 Acknowledgements

- [Meta AI](https://ai.meta.com) — for the `facebook/bart-large-cnn` model
- [HuggingFace](https://huggingface.co) — for the Transformers library
- [PyMuPDF](https://pymupdf.readthedocs.io) — for PDF processing
- [Flask](https://flask.palletsprojects.com) — for the lightweight backend

---

<div align="center">

<br/>

## 👤 Author

<img src="https://github.com/TUSHARTAMRAKAR.png" width="100" style="border-radius: 50%"/>

### Tushar Tamrakar

*Full-stack developer & AI enthusiast. Building real things, learning every day.*

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-TUSHARTAMRAKAR-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/TUSHARTAMRAKAR)

<br/>

---

<br/>

**If SummarAI helped you or impressed you — drop a ⭐ on the repo!**

*It takes 2 seconds and means the world to an indie developer.*

<br/>

```
◈ Built from scratch. Line by line. With ❤️ by Tushar.
```

<br/>

</div>
