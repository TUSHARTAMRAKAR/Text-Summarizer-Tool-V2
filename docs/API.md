# API Documentation — SummarAI

Base URL: `http://localhost:5000`

---

## Endpoints

### POST /api/summarize
Summarize text using NLP.

**Request:**
```json
{ "text": "...", "length": "medium", "method": "abstractive" }
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

**Length options:** `short` (30–80 tokens), `medium` (80–180 tokens), `long` (180–350 tokens)

**Method options:** `abstractive` (BART model), `extractive` (TF-IDF scoring)

**Error codes:**
- `400` — Text missing, too short (<50 chars), or too long (>50,000 chars)
- `500` — Internal server error

---

### GET /api/health
Returns server and model status.

```json
{ "status": "healthy", "model_loaded": true, "version": "1.0.0" }
```

---

### GET /api/sample
Returns a built-in sample article for demo purposes.

```json
{ "sample_text": "Artificial intelligence (AI) is transforming..." }
```
