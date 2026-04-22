<div align="center">

<br/>

# ◈ SummarAI — V2
## Full AI-Powered Text Summarization Tool

<p align="center">
  <em>The complete version — runs the full BART transformer model locally.</em><br/>
  <em>Both Abstractive (AI) and Extractive (TF-IDF) summarization, fully unlocked.</em>
</p>

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-BART--Large--CNN-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/facebook/bart-large-cnn)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.2-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-8B5CF6?style=for-the-badge)]()

<br/>

### 📦 [V1 — Hosted Version](https://github.com/TUSHARTAMRAKAR/Text-Summarizer-Tool) &nbsp;|&nbsp; 🌐 [Live Demo (V1)](https://summari-84uc.onrender.com) &nbsp;|&nbsp; 📖 [API Docs](docs/API.md)

<br/>

> ⚠️ **V2 is designed to run locally.** It loads the full `facebook/bart-large-cnn` model (~1.6GB)  
> which requires ~2GB RAM — beyond free cloud hosting limits.  
> For the hosted version, see [SummarAI V1](https://github.com/TUSHARTAMRAKAR/Text-Summarizer-Tool).

</div>

---

## 📌 V1 vs V2 — What's the Difference?

| Feature | V1 (Hosted) | V2 (Local) |
|---|---|---|
| 🌐 **Deployment** | Live on Render (free tier) | Run locally on your machine |
| 🧠 **Abstractive (BART)** | ❌ Disabled (RAM limit) | ✅ Fully working |
| ✂️ **Extractive (TF-IDF)** | ✅ Working | ✅ Working |
| 💾 **RAM Required** | < 512MB | ~2GB |
| ⚡ **Summary Quality** | Good (extractive) | Best (full AI model) |
| 🔗 **Access** | Browser, anywhere | `localhost:5000` |

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **Full Abstractive Summarization** | `facebook/bart-large-cnn` — reads, understands, and rewrites text like a human |
| ✂️ **Extractive Summarization** | Custom TF-IDF engine — fast, offline, no model needed |
| 📏 **3 Summary Lengths** | Short, Medium, Long — full control over output detail |
| 📊 **Live Statistics** | Compression ratio, word counts, method used |
| 📋 **One-Click Copy** | Copy summary to clipboard instantly |
| 🎯 **Built-in Demo Article** | Try it immediately with zero setup |
| 🌐 **REST API** | 3 clean JSON endpoints — integrate anywhere |

---

## 🗂️ Project Structure

```
Text-Summarizer-Tool-V2/
│
├── 📂 backend/
│   ├── app.py              # Flask app — API routes and server config
│   └── summarizer.py       # Full NLP engine — BART + TF-IDF, no restrictions
│
├── 📂 frontend/
│   ├── templates/
│   │   └── index.html      # Main web interface
│   └── static/
│       ├── css/style.css   # Dark editorial UI theme
│       └── js/main.js      # Frontend logic and API calls
│
├── 📂 tests/
│   └── test_summarizer.py  # Unit + integration tests (pytest)
│
├── 📂 docs/
│   └── API.md              # Full API reference
│
├── requirements.txt        # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### System Requirements

| Requirement | Minimum |
|---|---|
| **Python** | 3.10 or higher |
| **RAM** | 4GB recommended (2GB minimum) |
| **Disk Space** | ~3GB free (model cache + dependencies) |
| **Internet** | Required on first run (model download) |

---

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/TUSHARTAMRAKAR/Text-Summarizer-Tool-V2.git
cd Text-Summarizer-Tool-V2
```

**2. Create virtual environment**

```bash
python -m venv venv
```

**3. Activate it**

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Run the app**

```bash
cd backend
python app.py
```

**6. Open in browser**

```
http://localhost:5000
```

> ⏳ **First run:** The BART model (~1.6GB) downloads automatically and is cached locally.  
> This takes 5–15 minutes depending on your internet. Every run after that is instant.

---

## 🧠 How Abstractive Summarization Works (BART)

```
Your Article Text
        ↓
  BART Encoder
  (reads every word, builds deep contextual understanding)
        ↓
  BART Decoder
  (generates a brand new summary, word by word)
        ↓
  Fresh Human-like Summary
  (completely new sentences — not copied from original)
```

**`facebook/bart-large-cnn`** was trained by Meta AI on 300,000+ CNN and DailyMail news articles paired with human-written summaries. It learned to compress information exactly the way a journalist would.

---

## 🔌 API Reference

Base URL: `http://localhost:5000`

### `POST /api/summarize`

```json
{
  "text": "Your article here...",
  "length": "medium",
  "method": "abstractive"
}
```

**Response:**
```json
{
  "success": true,
  "summary": "...",
  "original_word_count": 500,
  "summary_word_count": 82,
  "compression_ratio": "84%",
  "method_used": "abstractive"
}
```

### `GET /api/health`
```json
{ "status": "healthy", "model_loaded": true, "version": "2.0.0" }
```

### `GET /api/sample`
Returns a built-in demo article.

Full docs → [`docs/API.md`](docs/API.md)

---

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend** | Python 3.10+, Flask 3.0 |
| **AI Model** | HuggingFace Transformers — `facebook/bart-large-cnn` |
| **Extractive NLP** | Custom TF-IDF (no extra libraries) |
| **Testing** | pytest |

---

## 🗺️ Roadmap

- [x] Full BART abstractive summarization
- [x] TF-IDF extractive summarization
- [x] Beautiful responsive web UI
- [x] REST API with JSON responses
- [x] Unit + integration test coverage
- [ ] PDF upload and summarization
- [ ] Summarize from URL
- [ ] Export summary as .txt / .pdf
- [ ] GPU acceleration support
- [ ] Multi-language summarization

---

## 🤝 Contributing

1. Fork the repo
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "feat: your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

<div align="center">

<br/>

## 👤 Author

### Tushar Tamrakar

[![GitHub](https://img.shields.io/badge/GitHub-TUSHARTAMRAKAR-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/TUSHARTAMRAKAR)

<br/>

*V2 — The full local version with complete AI capabilities.*

---

⭐ **If this helped you, give it a star!**

<sub>Made with ❤️ by Tushar Tamrakar</sub>

</div>
