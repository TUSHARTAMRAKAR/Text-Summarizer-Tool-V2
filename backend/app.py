"""
SummarAI V2 - Flask Backend
Features: Text, PDF, URL summarization + Export
"""

from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import logging
import os
import sys
import io
import re
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from summarizer import TextSummarizer

# ─── App Setup ────────────────────────────────────────────────────────────────
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)
CORS(app)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

logger.info("🔄 Loading summarization model...")
summarizer = TextSummarizer()
logger.info("✅ Model loaded successfully!")


# ─── Helper: Extract text from PDF ───────────────────────────────────────────
def extract_pdf_text(file_bytes: bytes) -> str:
    """Extract text from a PDF file using PyMuPDF (fitz)."""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except ImportError:
        raise RuntimeError("PyMuPDF not installed. Run: pip install pymupdf")
    except Exception as e:
        raise RuntimeError(f"Could not read PDF: {str(e)}")


# ─── Helper: Extract text from URL ───────────────────────────────────────────
def extract_url_text(url: str) -> str:
    """Scrape and extract clean article text from a URL."""
    try:
        import requests
        from bs4 import BeautifulSoup

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "ads"]):
            tag.decompose()

        # Try to find article content first
        article = soup.find("article") or soup.find("main") or soup.find("body")
        paragraphs = article.find_all("p") if article else soup.find_all("p")

        text = " ".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 40)

        if not text:
            text = soup.get_text(separator=" ", strip=True)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    except ImportError:
        raise RuntimeError("Required packages not installed. Run: pip install requests beautifulsoup4")
    except Exception as e:
        raise RuntimeError(f"Could not fetch URL: {str(e)}")


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# ─── Summarize Text ───────────────────────────────────────────────────────────
@app.route("/api/summarize", methods=["POST"])
def summarize():
    """Summarize plain text input."""
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"success": False, "error": "No text provided."}), 400

        text   = data["text"].strip()
        length = data.get("length", "medium")
        method = data.get("method", "abstractive")

        if len(text) < 50:
            return jsonify({"success": False, "error": "Text is too short. Please provide at least 50 characters."}), 400
        if len(text) > 50000:
            return jsonify({"success": False, "error": "Text is too long. Maximum 50,000 characters allowed."}), 400

        logger.info(f"📝 Summarizing text | {len(text)} chars | {length} | {method}")
        result = summarizer.summarize(text, length=length, method=method)
        return jsonify(result)

    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return jsonify({"success": False, "error": "An internal error occurred."}), 500


# ─── Summarize PDF ────────────────────────────────────────────────────────────
@app.route("/api/summarize-pdf", methods=["POST"])
def summarize_pdf():
    """
    Upload a PDF file and summarize its content.
    Form data: file (PDF), length, method
    """
    try:
        if "file" not in request.files:
            return jsonify({"success": False, "error": "No PDF file uploaded."}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"success": False, "error": "No file selected."}), 400
        if not file.filename.lower().endswith(".pdf"):
            return jsonify({"success": False, "error": "Only PDF files are supported."}), 400

        length = request.form.get("length", "medium")
        method = request.form.get("method", "abstractive")

        # Read PDF bytes and extract text
        file_bytes = file.read()
        if len(file_bytes) > 10 * 1024 * 1024:  # 10MB limit
            return jsonify({"success": False, "error": "PDF too large. Maximum size is 10MB."}), 400

        logger.info(f"📄 Processing PDF: {file.filename} ({len(file_bytes)} bytes)")
        text = extract_pdf_text(file_bytes)

        if not text or len(text) < 50:
            return jsonify({"success": False, "error": "Could not extract text from PDF. The file may be scanned or image-based."}), 400

        logger.info(f"✅ Extracted {len(text)} characters from PDF")
        result = summarizer.summarize(text, length=length, method=method)
        result["source"] = "pdf"
        result["filename"] = file.filename
        return jsonify(result)

    except RuntimeError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except Exception as e:
        logger.error(f"❌ PDF error: {str(e)}")
        return jsonify({"success": False, "error": "Failed to process PDF."}), 500


# ─── Summarize URL ────────────────────────────────────────────────────────────
@app.route("/api/summarize-url", methods=["POST"])
def summarize_url():
    """
    Fetch an article from a URL and summarize it.
    Request JSON: { "url": "...", "length": "medium", "method": "abstractive" }
    """
    try:
        data = request.get_json()
        if not data or "url" not in data:
            return jsonify({"success": False, "error": "No URL provided."}), 400

        url    = data["url"].strip()
        length = data.get("length", "medium")
        method = data.get("method", "abstractive")

        if not url.startswith(("http://", "https://")):
            return jsonify({"success": False, "error": "Invalid URL. Must start with http:// or https://"}), 400

        logger.info(f"🔗 Fetching URL: {url}")
        text = extract_url_text(url)

        if not text or len(text) < 50:
            return jsonify({"success": False, "error": "Could not extract enough text from the URL. The page may be behind a paywall or login."}), 400

        logger.info(f"✅ Extracted {len(text)} characters from URL")
        result = summarizer.summarize(text, length=length, method=method)
        result["source"] = "url"
        result["url"] = url
        return jsonify(result)

    except RuntimeError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except Exception as e:
        logger.error(f"❌ URL error: {str(e)}")
        return jsonify({"success": False, "error": "Failed to fetch URL."}), 500


# ─── Export Summary ───────────────────────────────────────────────────────────
@app.route("/api/export", methods=["POST"])
def export_summary():
    """
    Export a summary as .txt or .pdf file.
    Request JSON: { "summary": "...", "format": "txt" | "pdf", "original_word_count": 500, ... }
    """
    try:
        data = request.get_json()
        if not data or "summary" not in data:
            return jsonify({"success": False, "error": "No summary to export."}), 400

        summary       = data["summary"]
        export_format = data.get("format", "txt").lower()
        method_used   = data.get("method_used", "unknown")
        orig_words    = data.get("original_word_count", "N/A")
        summ_words    = data.get("summary_word_count", "N/A")
        compression   = data.get("compression_ratio", "N/A")

        if export_format == "txt":
            content = f"""SummarAI — Text Summary
{'='*50}
Method:           {method_used.capitalize()}
Original words:   {orig_words}
Summary words:    {summ_words}
Compression:      {compression}
{'='*50}

SUMMARY:

{summary}

{'='*50}
Generated by SummarAI V2 — github.com/TUSHARTAMRAKAR
"""
            buf = io.BytesIO(content.encode("utf-8"))
            buf.seek(0)
            return send_file(
                buf,
                mimetype="text/plain",
                as_attachment=True,
                download_name="summary.txt"
            )

        elif export_format == "pdf":
            try:
                import fitz
                doc = fitz.open()
                page = doc.new_page()

                # Title
                page.insert_text((50, 60), "SummarAI — Text Summary", fontsize=18, fontname="helv")
                page.draw_line((50, 75), (545, 75))

                # Meta info
                page.insert_text((50, 95),  f"Method:         {method_used.capitalize()}", fontsize=10)
                page.insert_text((50, 112), f"Original words: {orig_words}", fontsize=10)
                page.insert_text((50, 129), f"Summary words:  {summ_words}", fontsize=10)
                page.insert_text((50, 146), f"Compression:    {compression}", fontsize=10)
                page.draw_line((50, 160), (545, 160))

                # Summary heading
                page.insert_text((50, 180), "SUMMARY:", fontsize=12, fontname="helv")

                # Summary text — word wrap manually
                words = summary.split()
                lines, line = [], []
                for word in words:
                    line.append(word)
                    if len(" ".join(line)) > 80:
                        lines.append(" ".join(line[:-1]))
                        line = [word]
                if line:
                    lines.append(" ".join(line))

                y = 200
                for text_line in lines:
                    if y > 750:
                        page = doc.new_page()
                        y = 60
                    page.insert_text((50, y), text_line, fontsize=11)
                    y += 16

                # Footer
                page.insert_text((50, 800), "Generated by SummarAI V2 — github.com/TUSHARTAMRAKAR", fontsize=8)

                buf = io.BytesIO(doc.write())
                doc.close()
                buf.seek(0)
                return send_file(
                    buf,
                    mimetype="application/pdf",
                    as_attachment=True,
                    download_name="summary.pdf"
                )

            except ImportError:
                return jsonify({"success": False, "error": "PDF export requires PyMuPDF. Run: pip install pymupdf"}), 500

        else:
            return jsonify({"success": False, "error": "Invalid format. Use 'txt' or 'pdf'."}), 400

    except Exception as e:
        logger.error(f"❌ Export error: {str(e)}")
        return jsonify({"success": False, "error": "Export failed."}), 500


# ─── Health & Sample ──────────────────────────────────────────────────────────
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": summarizer.is_ready(),
        "version": "2.0.0",
        "features": ["text", "pdf", "url", "export"]
    })


@app.route("/api/sample", methods=["GET"])
def sample_text():
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
    port  = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") != "production"
    app.run(debug=debug, host="0.0.0.0", port=port)
