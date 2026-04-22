/**
 * main.js — SummarAI Frontend Logic
 * Handles: toggle controls, API calls, state management, copy, word count
 */

// ── DOM Elements ──────────────────────────────────────────────────────────────
const inputText     = document.getElementById("inputText");
const summarizeBtn  = document.getElementById("summarizeBtn");
const clearBtn      = document.getElementById("clearBtn");
const copyBtn       = document.getElementById("copyBtn");
const loadSampleBtn = document.getElementById("loadSampleBtn");
const inputCounter  = document.getElementById("inputCounter");
const outputCounter = document.getElementById("outputCounter");

// States
const emptyState    = document.getElementById("emptyState");
const loadingState  = document.getElementById("loadingState");
const resultState   = document.getElementById("resultState");
const errorState    = document.getElementById("errorState");

// Result elements
const summaryText   = document.getElementById("summaryText");
const statsBar      = document.getElementById("statsBar");
const errorMsg      = document.getElementById("errorMsg");

// ── App State ─────────────────────────────────────────────────────────────────
let selectedLength = "medium";
let selectedMethod = "abstractive";
let isLoading      = false;

// ── Toggle Controls ───────────────────────────────────────────────────────────
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

// ── Word Counter ──────────────────────────────────────────────────────────────
inputText.addEventListener("input", () => {
  const words = countWords(inputText.value);
  inputCounter.textContent = `${words} word${words !== 1 ? "s" : ""}`;
});

function countWords(text) {
  return text.trim() === "" ? 0 : text.trim().split(/\s+/).length;
}

// ── Clear Button ──────────────────────────────────────────────────────────────
clearBtn.addEventListener("click", () => {
  inputText.value = "";
  inputCounter.textContent = "0 words";
  showState("empty");
  copyBtn.style.display = "none";
  outputCounter.textContent = "— words";
});

// ── Load Sample ───────────────────────────────────────────────────────────────
loadSampleBtn.addEventListener("click", async () => {
  loadSampleBtn.textContent = "Loading…";
  loadSampleBtn.disabled = true;

  try {
    const res  = await fetch("/api/sample");
    const data = await res.json();
    inputText.value = data.sample_text;
    const words = countWords(data.sample_text);
    inputCounter.textContent = `${words} words`;
  } catch (e) {
    console.error("Failed to load sample:", e);
  } finally {
    loadSampleBtn.innerHTML = `<span>Load Sample Article</span><span class="btn-arrow">↗</span>`;
    loadSampleBtn.disabled = false;
  }
});

// ── Summarize ─────────────────────────────────────────────────────────────────
summarizeBtn.addEventListener("click", summarize);

inputText.addEventListener("keydown", e => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") summarize();
});

async function summarize() {
  if (isLoading) return;

  const text = inputText.value.trim();
  if (!text) {
    showError("Please paste some text first.");
    return;
  }
  if (text.length < 50) {
    showError("Text is too short. Paste a longer article.");
    return;
  }

  isLoading = true;
  summarizeBtn.classList.add("loading");
  summarizeBtn.querySelector(".btn-text").textContent = "WAIT…";
  showState("loading");
  copyBtn.style.display = "none";

  try {
    const response = await fetch("/api/summarize", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text:   text,
        length: selectedLength,
        method: selectedMethod
      })
    });

    const data = await response.json();

    if (!data.success) {
      showError(data.error || "Summarization failed. Please try again.");
      return;
    }

    displayResult(data);

  } catch (err) {
    console.error("API error:", err);
    showError("Could not connect to the server. Is Flask running?");
  } finally {
    isLoading = false;
    summarizeBtn.classList.remove("loading");
    summarizeBtn.querySelector(".btn-text").textContent = "SUMMARIZE";
  }
}

// ── Display Result ────────────────────────────────────────────────────────────
function displayResult(data) {
  summaryText.textContent = data.summary;

  const words = countWords(data.summary);
  outputCounter.textContent = `${words} words`;

  statsBar.innerHTML = `
    <div class="stat-item">
      <span class="stat-label">Original</span>
      <span class="stat-value">${data.original_word_count} words</span>
    </div>
    <div class="stat-item">
      <span class="stat-label">Summary</span>
      <span class="stat-value">${data.summary_word_count} words</span>
    </div>
    <div class="stat-item">
      <span class="stat-label">Reduced by</span>
      <span class="stat-value">${data.compression_ratio}</span>
    </div>
    <div class="stat-item">
      <span class="stat-label">Method</span>
      <span class="stat-value">${capitalize(data.method_used)}</span>
    </div>
  `;

  showState("result");
  copyBtn.style.display = "inline-flex";
}

// ── Copy to Clipboard ─────────────────────────────────────────────────────────
copyBtn.addEventListener("click", async () => {
  const text = summaryText.textContent;
  if (!text) return;

  try {
    await navigator.clipboard.writeText(text);
    copyBtn.textContent = "✓ Copied!";
    setTimeout(() => { copyBtn.innerHTML = "⎘ Copy"; }, 2000);
  } catch {
    copyBtn.textContent = "⚠ Failed";
    setTimeout(() => { copyBtn.innerHTML = "⎘ Copy"; }, 2000);
  }
});

// ── State Management ──────────────────────────────────────────────────────────
function showState(state) {
  emptyState.style.display   = state === "empty"   ? "flex" : "none";
  loadingState.style.display = state === "loading" ? "flex" : "none";
  resultState.style.display  = state === "result"  ? "flex" : "none";
  errorState.style.display   = state === "error"   ? "flex" : "none";
}

function showError(msg) {
  errorMsg.textContent = msg;
  showState("error");
}

// ── Utils ─────────────────────────────────────────────────────────────────────
function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// ── Init ──────────────────────────────────────────────────────────────────────
showState("empty");
