# ◈ SummarAI — Text Summarization Tool

> Turn thousands of words into clarity. A beautiful, full-stack web app that summarizes lengthy articles using state-of-the-art NLP.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

---

## 📸 Preview

```
┌─────────────────────────────────────────┐
│  ◈ SummarAI                             │
├─────────────────┬────────┬──────────────┤
│                 │        │              │
│  01 INPUT TEXT  │  SUM-  │  02 SUMMARY  │
│                 │  MAR-  │              │
│  Paste your     │  IZE   │  Your con-   │
│  article here…  │   ⟶    │  cise summ-  │
│                 │        │  ary appears │
└─────────────────┴────────┴──────────────┘
│ Original: 500 words │ Summary: 82 words │ Reduced by: 84% │
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **Abstractive Summarization** | Uses `facebook/bart-large-cnn` to rewrite text in its own words |
| ✂️ **Extractive Summarization** | TF-IDF sentence scoring — picks the most important original sentences |
| 📏 **3 Summary Lengths** | Short, Medium, Long — control how much detail you want |
| 📊 **Statistics** | Shows word count, compression ratio, and method used |
| 📋 **One-click Copy** | Copy your summary to clipboard instantly |
| 🎯 **Sample Article** | Built-in demo article to try it out immediately |
| 💯 **100% Free** | No paid APIs, no subscriptions, runs fully locally |

---

## 🗂️ Project Structure

```
text-summarizer-tool/
│
├── backend/
│   ├── app.py              # Flask application & API routes
│   └── summarizer.py       # Core NLP summarization engine
│
├── frontend/
│   ├── templates/
│   │   └── index.html      # Main web interface
│   └── static/
│       ├── css/
│       │   └── style.css   # Styling (dark editorial theme)
│       └── js/
│           └── main.js     # Frontend logic & API calls
│
├── tests/
│   └── test_summarizer.py  # Unit tests (pytest)
│
├── docs/
│   └── API.md              # API endpoint documentation
│
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/text-summarizer-tool.git
cd text-summarizer-tool
```

### 2. Set Up a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ **Note:** The first run downloads the `facebook/bart-large-cnn` model (~1.6GB). This only happens once — it's cached locally after that.

### 4. Run the App

```bash
cd backend
python app.py
```

### 5. Open in Browser

```
http://localhost:5000
```

---

## 🔌 API Reference

### `POST /api/summarize`

Summarize a piece of text.

**Request Body:**
```json
{
  "text": "Your long article text here...",
  "length": "medium",
  "method": "abstractive"
}
```

| Parameter | Type | Options | Default |
|---|---|---|---|
| `text` | string | Any text (50–50,000 chars) | required |
| `length` | string | `short`, `medium`, `long` | `medium` |
| `method` | string | `abstractive`, `extractive` | `abstractive` |

**Success Response:**
```json
{
  "success": true,
  "summary": "AI is transforming industries...",
  "original_word_count": 500,
  "summary_word_count": 82,
  "compression_ratio": "84%",
  "method_used": "abstractive"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Text is too short. Please provide at least 50 characters."
}
```

---

### `GET /api/health`

Check if the server and model are loaded.

```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

---

### `GET /api/sample`

Returns a sample article for demo purposes.

---

## 🧪 Running Tests

```bash
# From the project root
pip install pytest
python -m pytest tests/ -v
```

---

## 🧠 How It Works

### Abstractive Summarization (BART)
- Uses `facebook/bart-large-cnn`, a transformer model fine-tuned on CNN/DailyMail news articles
- The model **reads and understands** the text, then **writes a new summary** in its own words
- Like how a human would read and then explain it to someone else
- Best for natural, human-sounding summaries

### Extractive Summarization (TF-IDF)
- Scores every sentence by the **importance of the words it contains**
- Uses TF-IDF (Term Frequency–Inverse Document Frequency) weighting
- Picks the **top-ranked sentences** from the original text
- Faster, no model required, works offline always
- Best for factual, verbatim excerpts

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend** | Python 3.10+, Flask 3.0 |
| **NLP Model** | HuggingFace Transformers — `facebook/bart-large-cnn` |
| **Extractive NLP** | Custom TF-IDF implementation (no extra libraries) |
| **Testing** | pytest |

---

## 📝 What I Learned

Building this project taught me:
- How **NLP summarization** works (extractive vs abstractive)
- How to use **HuggingFace Transformers** pipeline for ML inference
- How to build a **REST API with Flask**
- How to connect a **frontend to a Python backend**
- How to write **unit tests** with pytest
- How to structure a **production-grade project**

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Your Name**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)

---

> ⭐ If you found this useful, consider giving it a star!
