let parsedProblem = null;
let solvedResult = null;

document.getElementById("inputType").addEventListener("change", (e) => {
  const type = e.target.value;
  document.getElementById("textInput").style.display =
    type === "text" ? "block" : "none";
  document.getElementById("fileInput").style.display =
    type !== "text" ? "block" : "none";
});

// ─────────────────────────────────────────────
// PARSE INPUT
// ─────────────────────────────────────────────
async function parseInput() {
  const inputType = document.getElementById("inputType").value;

  const text = document
    .getElementById("textInput")
    .value
    .replace(/\n+/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  const fileInput = document.getElementById("fileInput");

  const formData = new FormData();
  formData.append("input_type", inputType);

  if (inputType === "text") {
    formData.append("text", text);
  } else {
    if (!fileInput.files.length) {
      alert("Upload a file");
      return;
    }
    formData.append("file", fileInput.files[0]);
  }

  const res = await fetch("/parse", {
    method: "POST",
    body: formData
  });

  const data = await res.json();

  parsedProblem = data.parsed_problem;
  document.getElementById("parsedOutput").textContent =
    JSON.stringify(parsedProblem, null, 2);
}

// ─────────────────────────────────────────────
// SOLVE (MULTI-PROBLEM)
// ─────────────────────────────────────────────
async function solveProblem() {
  if (!parsedProblem) {
    alert("Parse first");
    return;
  }

  const res = await fetch("/solve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(parsedProblem)
  });

  const data = await res.json();
  solvedResult = data;

  renderResults(data);
}

// ─────────────────────────────────────────────
// RENDER RESULTS (CORRECTLY SPLIT)
// ─────────────────────────────────────────────
function renderResults(data) {
  const answerTextEl = document.getElementById("answerText");
  const answerLatexEl = document.getElementById("answerLatex");
  const ctxEl = document.getElementById("supportingContext");
  const sysInfoEl = document.getElementById("systemInfo");

  // Reset everything
  answerTextEl.innerHTML = "";
  answerLatexEl.innerHTML = "";
  ctxEl.innerHTML = "";
  sysInfoEl.textContent = "";

  if (!data.results || data.results.length === 0) {
    answerTextEl.textContent = "No results returned.";
    return;
  }

  sysInfoEl.textContent = `Total problems solved: ${data.total_problems}`;

  /* ======================================================
     FINAL RESULT COLUMN → ANSWERS ONLY
     ====================================================== */
  data.results.forEach((item, index) => {
    const block = document.createElement("div");
    block.className = "result-block";

    block.innerHTML = `
      <p><strong>Q${index + 1}:</strong> ${item.question}</p>
      <p><strong>Answer:</strong> ${item.final_answer.text}</p>
      <p class="source">Source: ${item.source?.answer || item.source}</p>
    `;

    if (item.final_answer.latex) {
      const latexDiv = document.createElement("div");
      latexDiv.innerHTML = `$$${item.final_answer.latex}$$`;
      block.appendChild(latexDiv);
    }

    answerTextEl.appendChild(block);
  });

  /* ======================================================
     SUPPORTING CONTEXT → EXPLANATIONS ONLY
     ====================================================== */
  data.results.forEach((item, index) => {
    if (!item.explanation) return;

    const expBlock = document.createElement("div");
    expBlock.className = "result-block";

    expBlock.innerHTML = `
      <p><strong>Q${index + 1} – Explanation:</strong></p>
      <p>${item.explanation}</p>
      <p class="source">Source: ${item.source?.explanation || item.source}</p>
    `;

    ctxEl.appendChild(expBlock);
  });

  // Re-render MathJax
  if (window.MathJax) {
    MathJax.typesetPromise();
  }
}

// ─────────────────────────────────────────────
// FEEDBACK
// ─────────────────────────────────────────────
async function sendFeedback(type) {
  if (!parsedProblem || !solvedResult) {
    alert("Nothing to submit");
    return;
  }

  await fetch("/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      problem: parsedProblem,
      solution: solvedResult,
      feedback: type
    })
  });

  alert("Feedback saved");
}
