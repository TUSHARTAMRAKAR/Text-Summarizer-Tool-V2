"""
tests/test_summarizer.py — Unit Tests for TextSummarizer
Run with: python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pytest
from summarizer import TextSummarizer


# ── Fixtures ──────────────────────────────────────────────────────────────────
@pytest.fixture(scope="module")
def summarizer():
    """Create a single summarizer instance for all tests."""
    return TextSummarizer()


SAMPLE_TEXT = """
Artificial intelligence (AI) is transforming industries across the globe. 
From healthcare to finance, AI-powered systems are automating complex tasks 
and uncovering insights from vast datasets. In healthcare, AI algorithms 
diagnose diseases with remarkable accuracy. In finance, fraud detection systems 
analyze patterns in real time. In education, adaptive platforms personalize 
curriculum for individual students. Despite remarkable advances, AI also presents 
significant challenges including job displacement, algorithmic bias, and data 
privacy concerns. Ensuring responsible and equitable AI development remains 
one of the most pressing challenges of our era.
"""

SHORT_TEXT = "AI is great."


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestExtractive:
    """Tests for the extractive summarization method."""

    def test_extractive_returns_dict(self, summarizer):
        result = summarizer.summarize(SAMPLE_TEXT, method="extractive")
        assert isinstance(result, dict)

    def test_extractive_success_flag(self, summarizer):
        result = summarizer.summarize(SAMPLE_TEXT, method="extractive")
        assert result["success"] is True

    def test_extractive_has_summary(self, summarizer):
        result = summarizer.summarize(SAMPLE_TEXT, method="extractive")
        assert "summary" in result
        assert len(result["summary"]) > 0

    def test_extractive_method_label(self, summarizer):
        result = summarizer.summarize(SAMPLE_TEXT, method="extractive")
        assert result["method_used"] == "extractive"

    def test_extractive_word_counts(self, summarizer):
        result = summarizer.summarize(SAMPLE_TEXT, method="extractive")
        assert result["original_word_count"] > 0
        assert result["summary_word_count"] > 0
        assert result["summary_word_count"] <= result["original_word_count"]

    def test_extractive_short_length(self, summarizer):
        result = summarizer.summarize(SAMPLE_TEXT, length="short", method="extractive")
        medium = summarizer.summarize(SAMPLE_TEXT, length="medium", method="extractive")
        assert result["summary_word_count"] <= medium["summary_word_count"]

    def test_extractive_compression_ratio_format(self, summarizer):
        result = summarizer.summarize(SAMPLE_TEXT, method="extractive")
        assert "%" in result["compression_ratio"]

    def test_extractive_very_short_text(self, summarizer):
        """Very short texts should return as-is."""
        result = summarizer.summarize("Hello world. This is a test.", method="extractive")
        assert result["success"] is True


class TestWordCounting:
    """Tests for word count accuracy."""

    def test_original_word_count_accuracy(self, summarizer):
        text = "one two three four five"
        result = summarizer.summarize(text + " " * 50 + SAMPLE_TEXT, method="extractive")
        assert result["original_word_count"] > 0

    def test_compression_ratio_is_positive(self, summarizer):
        result = summarizer.summarize(SAMPLE_TEXT, method="extractive")
        ratio = int(result["compression_ratio"].replace("%", ""))
        assert 0 <= ratio <= 100


class TestEdgeCases:
    """Edge case handling tests."""

    def test_handles_multiline_text(self, summarizer):
        text = "\n".join([f"Sentence {i} with some content about topic {i}." for i in range(20)])
        result = summarizer.summarize(text, method="extractive")
        assert result["success"] is True

    def test_handles_extra_whitespace(self, summarizer):
        text = "  " + SAMPLE_TEXT + "   "
        result = summarizer.summarize(text, method="extractive")
        assert result["success"] is True

    def test_all_length_options(self, summarizer):
        for length in ["short", "medium", "long"]:
            result = summarizer.summarize(SAMPLE_TEXT, length=length, method="extractive")
            assert result["success"] is True

    def test_invalid_length_defaults_to_medium(self, summarizer):
        result = summarizer.summarize(SAMPLE_TEXT, length="invalid", method="extractive")
        assert result["success"] is True


class TestAPIEndpoints:
    """Tests for Flask API endpoints using test client."""

    @pytest.fixture(scope="class")
    def client(self):
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
        from app import app
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_health_endpoint(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.get_json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_sample_endpoint(self, client):
        response = client.get("/api/sample")
        assert response.status_code == 200
        data = response.get_json()
        assert "sample_text" in data
        assert len(data["sample_text"]) > 100

    def test_summarize_endpoint_valid(self, client):
        response = client.post("/api/summarize", json={
            "text": SAMPLE_TEXT,
            "length": "medium",
            "method": "extractive"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True

    def test_summarize_endpoint_no_text(self, client):
        response = client.post("/api/summarize", json={})
        assert response.status_code == 400

    def test_summarize_endpoint_too_short(self, client):
        response = client.post("/api/summarize", json={"text": "Hi"})
        assert response.status_code == 400

    def test_index_route(self, client):
        response = client.get("/")
        assert response.status_code == 200
