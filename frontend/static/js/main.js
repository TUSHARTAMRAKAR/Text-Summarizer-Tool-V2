/**
 * SummarAI V2 — main.js
 * Features: Text / PDF / URL input, Export (.txt & .pdf), Dark/Light mode, Summary History
 */

// ── DOM ───────────────────────────────────────────────────────────────────────
const inputText       = document.getElementById("inputText");
const urlInput        = document.getElementById("urlInput");
const pdfFileInput    = document.getElementById("pdfFileInput");
const pdfDropZone     = document.getElementById("pdfDropZone");
const pdfInfo         = document.getElementById("pdfInfo");
const summarizeBtn    = document.getElementById("summarizeBtn");
const clearBtn        = document.getElementById("clearBtn");
const copyBtn         = document.getElementById("copyBtn");
const exportTxtBtn    = document.getElementById("exportTxtBtn");
const exportPdfBtn    = document.getElementById("exportPdfBtn");
const loadSampleBtn   = document.getElementById("loadSampleBtn");
const themeToggle     = document.getElementById("themeToggle");
const inputCounter    = document.getElementById("inputCounter");
const outputCounter   = document.getElementById("outputCounter");
const inputPanelTitle = document.getElementById("inputPanelTitle");
const loadingMsg      = document.getElementById("loadingMsg");

// States
const emptyState   = document.getElementById("emptyState");
const loadingState = document.getElementById("loadingState");
const resultState  = document.getElementById("resultState");
const errorState   = document.getElementById("errorState");
const summaryText  = document.getElementById("summaryText");
const statsBar     = document.getElementById("statsBar");
const errorMsg     = document.getElementById("errorMsg");

// History
const historyList  = document.getElementById("historyList");
const historyCount = document.getElementById("historyCount");
const clearHistoryBtn = document.getElementById("clearHistoryBtn");

// ── App State ─────────────────────────────────────────────────────────────────
let selectedLength = "medium";
let selectedMethod = "abstractive";
let selectedSource = "text";
let isLoading      = false;
let lastResult     = null;
let selectedPdfFile = null;
let summaryHistory  = [];

// ── Theme ─────────────────────────────────────────────────────────────────────
const savedTheme = localStorage.getItem("summarai-theme") || "dark";
document.documentElement.setAttribute("data-theme", savedTheme);
updateThemeIcon(savedTheme);

themeToggle.addEventListener("click", () => {
  const current = document.documentElement.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("summarai-theme", next);
  updateThemeIcon(next);
});

function updateThemeIcon(theme) {
  themeToggle.querySelector(".theme-icon").textContent = theme === "dark" ? "☀️" : "🌙";
}

// ── Toggles ───────────────────────────────────────────────────────────────────
function initToggles(groupId, onSelect) {
  const group = document.getElementById(groupId);
  group.querySelectorAll(".toggle-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      group.querySelectorAll(".toggle-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      onSelect(btn.dataset.value);
    });
  });
}

initToggles("lengthToggle", val => { selectedLength = val; });
initToggles("methodToggle", val => { selectedMethod = val; });
initToggles("sourceToggle", val => {
  selectedSource = val;
  switchInputSource(val);
});

function switchInputSource(source) {
  document.querySelectorAll(".input-section").forEach(s => s.classList.remove("active"));
  document.getElementById(`${source}InputSection`).classList.add("active");

  const titles = { text: "INPUT TEXT", pdf: "UPLOAD PDF", url: "ARTICLE URL" };
  inputPanelTitle.textContent = titles[source];

  inputCounter.textContent = "0 words";
  showState("empty");
  copyBtn.style.display = "none";
  exportTxtBtn.style.display = "none";
  exportPdfBtn.style.display = "none";
}

// ── Word Counter ──────────────────────────────────────────────────────────────
inputText.addEventListener("input", () => {
  const w = countWords(inputText.value);
  inputCounter.textContent = `${w} word${w !== 1 ? "s" : ""}`;
});

function countWords(text) {
  return text.trim() === "" ? 0 : text.trim().split(/\s+/).length;
}

// ── Clear ─────────────────────────────────────────────────────────────────────
clearBtn.addEventListener("click", () => {
  inputText.value = "";
  urlInput.value = "";
  selectedPdfFile = null;
  pdfInfo.style.display = "none";
  pdfInfo.textContent = "";
  inputCounter.textContent = "0 words";
  outputCounter.textContent = "— words";
  showState("empty");
  copyBtn.style.display = "none";
  exportTxtBtn.style.display = "none";
  exportPdfBtn.style.display = "none";
  lastResult = null;
});

// ── Load Sample ───────────────────────────────────────────────────────────────
loadSampleBtn.addEventListener("click", async () => {
  loadSampleBtn.innerHTML = "<span>Loading…</span>";
  loadSampleBtn.disabled = true;

  // Switch to text mode
  document.getElementById("sourceToggle").querySelectorAll(".toggle-btn").forEach(b => {
    b.classList.remove("active");
    if (b.dataset.value === "text") b.classList.add("active");
  });
  switchInputSource("text");
  selectedSource = "text";

  try {
    const res  = await fetch("/api/sample");
    const data = await res.json();
    inputText.value = data.sample_text;
    inputCounter.textContent = `${countWords(data.sample_text)} words`;
  } catch (e) {
    console.error(e);
  } finally {
    loadSampleBtn.innerHTML = `<span>Load Sample</span><span class="btn-arrow">↗</span>`;
    loadSampleBtn.disabled = false;
  }
});

// ── PDF Drag & Drop ───────────────────────────────────────────────────────────
pdfDropZone.addEventListener("dragover", e => { e.preventDefault(); pdfDropZone.classList.add("dragover"); });
pdfDropZone.addEventListener("dragleave", () => pdfDropZone.classList.remove("dragover"));
pdfDropZone.addEventListener("drop", e => {
  e.preventDefault();
  pdfDropZone.classList.remove("dragover");
  const file = e.dataTransfer.files[0];
  if (file) handlePdfFile(file);
});

pdfFileInput.addEventListener("change", () => {
  if (pdfFileInput.files[0]) handlePdfFile(pdfFileInput.files[0]);
});

function handlePdfFile(file) {
  if (!file.name.toLowerCase().endsWith(".pdf")) {
    showError("Only PDF files are supported.");
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    showError("PDF too large. Maximum size is 10MB.");
    return;
  }
  selectedPdfFile = file;
  const sizeMB = (file.size / 1024 / 1024).toFixed(2);
  pdfInfo.textContent = `📄 ${file.name}  (${sizeMB} MB) — ready`;
  pdfInfo.style.display = "block";
  inputCounter.textContent = "PDF loaded";
}

// ── Summarize ─────────────────────────────────────────────────────────────────
summarizeBtn.addEventListener("click", summarize);

async function summarize() {
  if (isLoading) return;

  isLoading = true;
  summarizeBtn.classList.add("loading");
  summarizeBtn.querySelector(".btn-text").textContent = "WAIT…";
  copyBtn.style.display = "none";
  exportTxtBtn.style.display = "none";
  exportPdfBtn.style.display = "none";

  try {
    let result;

    if (selectedSource === "text") {
      result = await summarizeText();
    } else if (selectedSource === "pdf") {
      result = await summarizePdf();
    } else if (selectedSource === "url") {
      result = await summarizeUrl();
    }

    if (result) {
      lastResult = result;
      displayResult(result);
      addToHistory(result);
    }

  } finally {
    isLoading = false;
    summarizeBtn.classList.remove("loading");
    summarizeBtn.querySelector(".btn-text").textContent = "SUMMARIZE";
  }
}

// ── Text Summarization ────────────────────────────────────────────────────────
async function summarizeText() {
  const text = inputText.value.trim();
  if (!text) { showError("Please paste some text first."); return null; }
  if (text.length < 50) { showError("Text too short. Paste a longer article."); return null; }

  showState("loading");
  loadingMsg.textContent = "Analyzing text…";

  const res  = await fetch("/api/summarize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, length: selectedLength, method: selectedMethod })
  });
  const data = await res.json();
  if (!data.success) { showError(data.error); return null; }
  return data;
}

// ── PDF Summarization ─────────────────────────────────────────────────────────
async function summarizePdf() {
  if (!selectedPdfFile) { showError("Please upload a PDF file first."); return null; }

  showState("loading");
  loadingMsg.textContent = "Extracting PDF text…";

  const formData = new FormData();
  formData.append("file", selectedPdfFile);
  formData.append("length", selectedLength);
  formData.append("method", selectedMethod);

  const res  = await fetch("/api/summarize-pdf", { method: "POST", body: formData });
  const data = await res.json();
  if (!data.success) { showError(data.error); return null; }
  return data;
}

// ── URL Summarization ─────────────────────────────────────────────────────────
async function summarizeUrl() {
  const url = urlInput.value.trim();
  if (!url) { showError("Please paste a URL first."); return null; }
  if (!url.startsWith("http://") && !url.startsWith("https://")) {
    showError("Invalid URL. Must start with http:// or https://"); return null;
  }

  showState("loading");
  loadingMsg.textContent = "Fetching article…";

  const res  = await fetch("/api/summarize-url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, length: selectedLength, method: selectedMethod })
  });
  const data = await res.json();
  if (!data.success) { showError(data.error); return null; }
  return data;
}

// ── Display Result ────────────────────────────────────────────────────────────
function displayResult(data) {
  summaryText.textContent = data.summary;
  const words = countWords(data.summary);
  outputCounter.textContent = `${words} words`;

  let sourceTag = "";
  if (data.source === "pdf") sourceTag = `<div class="stat-item"><span class="stat-label">Source</span><span class="stat-value">📄 PDF</span></div>`;
  if (data.source === "url") sourceTag = `<div class="stat-item"><span class="stat-label">Source</span><span class="stat-value">🔗 URL</span></div>`;

  statsBar.innerHTML = `
    <div class="stat-item"><span class="stat-label">Original</span><span class="stat-value">${data.original_word_count} words</span></div>
    <div class="stat-item"><span class="stat-label">Summary</span><span class="stat-value">${data.summary_word_count} words</span></div>
    <div class="stat-item"><span class="stat-label">Reduced by</span><span class="stat-value">${data.compression_ratio}</span></div>
    <div class="stat-item"><span class="stat-label">Method</span><span class="stat-value">${capitalize(data.method_used)}</span></div>
    ${sourceTag}
  `;

  showState("result");
  copyBtn.style.display = "inline-flex";
  exportTxtBtn.style.display = "inline-flex";
  exportPdfBtn.style.display = "inline-flex";
}

// ── Copy ──────────────────────────────────────────────────────────────────────
copyBtn.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(summaryText.textContent);
    copyBtn.textContent = "✓ Copied!";
    setTimeout(() => { copyBtn.innerHTML = "⎘ Copy"; }, 2000);
  } catch {
    copyBtn.textContent = "⚠ Failed";
    setTimeout(() => { copyBtn.innerHTML = "⎘ Copy"; }, 2000);
  }
});

// ── Export ────────────────────────────────────────────────────────────────────
exportTxtBtn.addEventListener("click", () => exportSummary("txt"));
exportPdfBtn.addEventListener("click", () => exportSummary("pdf"));

async function exportSummary(format) {
  if (!lastResult) return;

  exportTxtBtn.textContent = "⏳";
  exportPdfBtn.textContent = "⏳";

  try {
    const res = await fetch("/api/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...lastResult, format })
    });

    if (!res.ok) {
      const err = await res.json();
      showError(err.error);
      return;
    }

    // Trigger download
    const blob = await res.blob();
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement("a");
    a.href     = url;
    a.download = `summary.${format}`;
    a.click();
    URL.revokeObjectURL(url);

  } catch (e) {
    showError("Export failed. Please try again.");
  } finally {
    exportTxtBtn.innerHTML = "↓ TXT";
    exportPdfBtn.innerHTML = "↓ PDF";
  }
}

// ── History ───────────────────────────────────────────────────────────────────
function addToHistory(result) {
  const entry = {
    id:         Date.now(),
    time:       new Date().toLocaleTimeString(),
    summary:    result.summary,
    method:     result.method_used,
    source:     result.source || "text",
    orig_words: result.original_word_count,
    summ_words: result.summary_word_count,
    compression: result.compression_ratio
  };

  summaryHistory.unshift(entry);
  if (summaryHistory.length > 10) summaryHistory.pop();
  renderHistory();
}

function renderHistory() {
  historyCount.textContent = `${summaryHistory.length} summar${summaryHistory.length === 1 ? "y" : "ies"}`;

  if (summaryHistory.length === 0) {
    historyList.innerHTML = `<div class="history-empty"><p>Your last 10 summaries will appear here</p></div>`;
    return;
  }

  historyList.innerHTML = summaryHistory.map(entry => `
    <div class="history-item" onclick="loadFromHistory(${entry.id})">
      <div class="history-item-meta">
        <span class="history-item-time">${entry.time}</span>
        <span class="history-item-method">${capitalize(entry.method)}</span>
        <span class="history-item-source">${sourceIcon(entry.source)} ${capitalize(entry.source)}</span>
      </div>
      <div class="history-item-preview">${entry.summary.substring(0, 120)}…</div>
      <div class="history-item-stats">${entry.orig_words}→${entry.summ_words}w<br/>${entry.compression}</div>
    </div>
  `).join("");
}

function loadFromHistory(id) {
  const entry = summaryHistory.find(e => e.id === id);
  if (!entry) return;

  summaryText.textContent = entry.summary;
  outputCounter.textContent = `${countWords(entry.summary)} words`;
  statsBar.innerHTML = `
    <div class="stat-item"><span class="stat-label">Original</span><span class="stat-value">${entry.orig_words} words</span></div>
    <div class="stat-item"><span class="stat-label">Summary</span><span class="stat-value">${entry.summ_words} words</span></div>
    <div class="stat-item"><span class="stat-label">Reduced by</span><span class="stat-value">${entry.compression}</span></div>
    <div class="stat-item"><span class="stat-label">Method</span><span class="stat-value">${capitalize(entry.method)}</span></div>
  `;
  lastResult = { summary: entry.summary, method_used: entry.method, original_word_count: entry.orig_words, summary_word_count: entry.summ_words, compression_ratio: entry.compression };
  showState("result");
  copyBtn.style.display = "inline-flex";
  exportTxtBtn.style.display = "inline-flex";
  exportPdfBtn.style.display = "inline-flex";
}

clearHistoryBtn.addEventListener("click", () => {
  summaryHistory = [];
  renderHistory();
});

// ── State Management ──────────────────────────────────────────────────────────
function showState(state) {
  emptyState.style.display   = state === "empty"   ? "flex" : "none";
  loadingState.style.display = state === "loading" ? "flex" : "none";
  resultState.style.display  = state === "result"  ? "flex" : "none";
  errorState.style.display   = state === "error"   ? "flex" : "none";
}

function showError(msg) {
  errorMsg.innerHTML = `<p>${msg}</p>`;
  showState("error");
}

// ── Utils ─────────────────────────────────────────────────────────────────────
function capitalize(str) { return str ? str.charAt(0).toUpperCase() + str.slice(1) : ""; }
function sourceIcon(src) { return src === "pdf" ? "📄" : src === "url" ? "🔗" : "✏️"; }

// ── Init ──────────────────────────────────────────────────────────────────────
showState("empty");
renderHistory();
