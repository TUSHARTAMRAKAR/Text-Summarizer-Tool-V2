"""
Text Summarization Tool - Flask Backend
Author: Your Name
Description: A web application that summarizes lengthy articles using
             NLP techniques powered by HuggingFace Transformers.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from summarizer import TextSummarizer

# ─── App Setup ────────────────────────────────────────────────────────────────
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)
CORS(app)

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ─── Load Summarizer (once at startup) ───────────────────────────────────────
logger.info("🔄 Loading summarization model... (this may take a moment on first run)")
summarizer = TextSummarizer()
logger.info("✅ Model loaded successfully!")


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main web interface."""
    return render_template("index.html")


@app.route("/api/summarize", methods=["POST"])
def summarize():
    """
    Summarize input text.

    Request JSON:
        {
            "text": "Your long article text here...",
            "length": "short" | "medium" | "long",
            "method": "abstractive" | "extractive"
        }

    Response JSON:
        {
            "success": true,
            "summary": "...",
            "original_word_count": 500,
            "summary_word_count": 80,
            "compression_ratio": "84%",
            "method_used": "abstractive"
        }
    """
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"success": False, "error": "No text provided."}), 400

        text = data["text"].strip()
        length = data.get("length", "medium")       # short / medium / long
        method = data.get("method", "abstractive")  # abstractive / extractive

        if len(text) < 50:
            return jsonify({"success": False, "error": "Text is too short. Please provide at least 50 characters."}), 400

        if len(text) > 50000:
            return jsonify({"success": False, "error": "Text is too long. Maximum 50,000 characters allowed."}), 400

        logger.info(f"📝 Summarizing {len(text)} chars | length={length} | method={method}")

        result = summarizer.summarize(text, length=length, method=method)

        logger.info(f"✅ Summary generated: {result['summary_word_count']} words")
        return jsonify(result)

    except Exception as e:
        logger.error(f"❌ Error during summarization: {str(e)}")
        return jsonify({"success": False, "error": "An internal error occurred. Please try again."}), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "model_loaded": summarizer.is_ready(),
        "version": "1.0.0"
    })


@app.route("/api/sample", methods=["GET"])
def sample_text():
    """Return a sample article for demo purposes."""
    sample = """Artificial intelligence (AI) is transforming industries across the globe at an unprecedented pace. 
From healthcare to finance, education to transportation, AI-powered systems are automating complex tasks, 
uncovering insights from vast datasets, and enabling capabilities that were once considered the realm of science fiction.

In healthcare, AI algorithms are now capable of diagnosing diseases from medical images with accuracy that rivals 
or even exceeds that of experienced physicians. Machine learning models trained on millions of X-rays, MRIs, and 
CT scans can detect early signs of cancer, heart disease, and neurological disorders, often catching conditions 
that human eyes might miss. This has the potential to revolutionize preventive care and early intervention.

The financial sector has also been deeply transformed by AI. High-frequency trading algorithms execute millions 
of transactions per second, while fraud detection systems analyze patterns in real time to flag suspicious activity. 
Robo-advisors now manage billions of dollars in assets, providing personalized investment strategies to retail 
investors who previously lacked access to professional financial advice.

In education, adaptive learning platforms use AI to personalize curriculum for individual students, identifying 
knowledge gaps and adjusting content difficulty in real time. This tailored approach has shown promising results 
in improving student outcomes, particularly for those who learn at different paces or have diverse learning needs.

Transportation is another domain experiencing an AI revolution. Self-driving vehicles, once a distant dream, 
are now being tested on public roads across multiple countries. AI systems process data from cameras, radar, 
and lidar sensors to navigate complex environments, potentially reducing accidents caused by human error and 
improving traffic flow in congested urban areas.

Despite these remarkable advances, AI also presents significant challenges and ethical considerations. Questions 
around job displacement, algorithmic bias, data privacy, and the concentration of power in the hands of a few 
technology giants are subjects of intense debate among policymakers, researchers, and the public. Ensuring that 
AI development proceeds in a responsible, equitable, and transparent manner remains one of the most pressing 
challenges of our time."""
    return jsonify({"sample_text": sample})


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
