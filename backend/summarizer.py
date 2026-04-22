"""
summarizer.py — Core NLP Summarization Engine
Supports two methods:
  1. Abstractive  — HuggingFace BART model (rewrites in its own words)
  2. Extractive   — TF-IDF + sentence scoring (picks best original sentences)
"""

import re
import math
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# ─── Length Configs ───────────────────────────────────────────────────────────
LENGTH_CONFIG = {
    "short":  {"min_tokens": 30,  "max_tokens": 80,  "extract_ratio": 0.15},
    "medium": {"min_tokens": 80,  "max_tokens": 180, "extract_ratio": 0.30},
    "long":   {"min_tokens": 180, "max_tokens": 350, "extract_ratio": 0.50},
}


class TextSummarizer:
    """
    Unified text summarizer supporting:
      - Abstractive summarization via facebook/bart-large-cnn
      - Extractive summarization via TF-IDF sentence scoring
    """

    def __init__(self):
        self._pipeline = None
        self._model_name = "facebook/bart-large-cnn"
        self._load_model()

    # ── Model Loading ──────────────────────────────────────────────────────────
    def _load_model(self):
        """Load the HuggingFace summarization pipeline."""
        try:
            from transformers import pipeline
            logger.info(f"Loading model: {self._model_name}")
            self._pipeline = pipeline(
                "summarization",
                model=self._model_name,
                device=-1          # CPU (no GPU required)
            )
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.warning(f"Could not load HuggingFace model: {e}")
            logger.warning("Falling back to extractive-only mode.")
            self._pipeline = None

    def is_ready(self) -> bool:
        """Return True if the abstractive model is available."""
        return self._pipeline is not None

    # ── Public API ─────────────────────────────────────────────────────────────
    def summarize(self, text: str, length: str = "medium", method: str = "abstractive") -> dict:
        """
        Summarize text.

        Args:
            text:   Input article text.
            length: 'short', 'medium', or 'long'.
            method: 'abstractive' or 'extractive'.

        Returns:
            dict with summary and metadata.
        """
        length = length if length in LENGTH_CONFIG else "medium"

        if method == "abstractive" and self._pipeline is not None:
            summary = self._abstractive(text, length)
            method_used = "abstractive"
        else:
            summary = self._extractive(text, length)
            method_used = "extractive"

        original_words = len(text.split())
        summary_words  = len(summary.split())
        compression    = round((1 - summary_words / max(original_words, 1)) * 100)

        return {
            "success": True,
            "summary": summary,
            "original_word_count": original_words,
            "summary_word_count": summary_words,
            "compression_ratio": f"{compression}%",
            "method_used": method_used,
        }

    # ── Abstractive (BART) ─────────────────────────────────────────────────────
    def _abstractive(self, text: str, length: str) -> str:
        """Use BART to generate an abstractive summary."""
        cfg = LENGTH_CONFIG[length]

        # BART has a 1024-token input limit — chunk if necessary
        chunks = self._chunk_text(text, max_chars=3000)
        summaries = []

        for chunk in chunks:
            if len(chunk.split()) < 30:
                continue
            try:
                result = self._pipeline(
                    chunk,
                    max_length=cfg["max_tokens"],
                    min_length=cfg["min_tokens"],
                    do_sample=False,
                    truncation=True
                )
                summaries.append(result[0]["summary_text"])
            except Exception as e:
                logger.error(f"Abstractive chunk failed: {e}")
                summaries.append(self._extractive(chunk, length))

        if not summaries:
            return self._extractive(text, length)

        combined = " ".join(summaries)

        # If multiple chunks, do a second-pass summary
        if len(chunks) > 1 and len(combined.split()) > cfg["max_tokens"]:
            try:
                result = self._pipeline(
                    combined,
                    max_length=cfg["max_tokens"],
                    min_length=cfg["min_tokens"],
                    do_sample=False,
                    truncation=True
                )
                return result[0]["summary_text"]
            except Exception:
                pass

        return combined

    # ── Extractive (TF-IDF) ────────────────────────────────────────────────────
    def _extractive(self, text: str, length: str) -> str:
        """Score sentences by TF-IDF weight and return the top-ranked ones."""
        cfg = LENGTH_CONFIG[length]
        ratio = cfg["extract_ratio"]

        sentences = self._split_sentences(text)
        if len(sentences) <= 3:
            return text.strip()

        # Build word frequency table (TF)
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        stop_words = self._stop_words()
        word_freq = {}
        for w in words:
            if w not in stop_words:
                word_freq[w] = word_freq.get(w, 0) + 1

        # Normalize frequencies
        max_freq = max(word_freq.values(), default=1)
        word_freq = {w: f / max_freq for w, f in word_freq.items()}

        # Score each sentence
        sentence_scores = {}
        for i, sent in enumerate(sentences):
            sent_words = re.findall(r'\b[a-z]{3,}\b', sent.lower())
            score = sum(word_freq.get(w, 0) for w in sent_words)
            # Slight boost for early sentences (they're often topic sentences)
            position_boost = 1.2 if i < 3 else 1.0
            sentence_scores[i] = score * position_boost

        # Pick top N sentences
        n = max(2, math.ceil(len(sentences) * ratio))
        top_indices = sorted(
            sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:n]
        )

        summary = " ".join(sentences[i] for i in top_indices)
        return summary.strip()

    # ── Helpers ────────────────────────────────────────────────────────────────
    def _chunk_text(self, text: str, max_chars: int = 3000) -> list:
        """Split text into chunks that respect paragraph boundaries."""
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        chunks, current = [], ""

        for para in paragraphs:
            if len(current) + len(para) < max_chars:
                current += " " + para
            else:
                if current:
                    chunks.append(current.strip())
                current = para

        if current:
            chunks.append(current.strip())

        return chunks if chunks else [text]

    def _split_sentences(self, text: str) -> list:
        """Basic sentence splitter."""
        text = re.sub(r'\s+', ' ', text)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 20]

    def _stop_words(self) -> set:
        return {
            "the","a","an","and","or","but","in","on","at","to","for","of",
            "with","by","from","is","was","are","were","be","been","being",
            "have","has","had","do","does","did","will","would","could","should",
            "may","might","shall","can","that","this","these","those","it","its",
            "they","their","there","then","than","so","if","as","not","also",
            "which","who","whom","what","when","where","how","about","after",
            "before","between","into","through","during","while","although",
            "because","since","until","whether","both","either","each","more",
            "most","other","such","no","nor","only","own","same","too","very",
        }
