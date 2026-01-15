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
// RENDER RESULTS (MULTI)
// ─────────────────────────────────────────────
function renderResults(data) {
  const answerTextEl = document.getElementById("answerText");
  const latexEl = document.getElementById("answerLatex");
  const ctxEl = document.getElementById("supportingContext");
  const sysInfoEl = document.getElementById("systemInfo");

  // Reset
  answerTextEl.innerHTML = "";
  latexEl.innerHTML = "";
  ctxEl.innerHTML = "";
  sysInfoEl.textContent = "";

  if (!data.results || data.results.length === 0) {
    answerTextEl.textContent = "No results returned.";
    return;
  }

  sysInfoEl.textContent = `Total problems solved: ${data.total_problems}`;

  data.results.forEach((item, index) => {
    // ───── Result Block
    const block = document.createElement("div");
    block.className = "result-block";

    // Question
    const q = document.createElement("p");
    q.innerHTML = `<strong>Q${index + 1}:</strong> ${item.question}`;
    block.appendChild(q);

    // Answer (Text)
    const a = document.createElement("p");
    a.innerHTML = `<strong>Answer:</strong> ${item.final_answer.text}`;
    block.appendChild(a);

    // Answer (LaTeX)
    if (item.final_answer.latex) {
      const latexDiv = document.createElement("div");
      latexDiv.innerHTML = `$$${item.final_answer.latex}$$`;
      block.appendChild(latexDiv);
    }

    // Source
    const src = document.createElement("p");
    src.className = "source";
    src.textContent = `Source: ${item.source}`;
    block.appendChild(src);

    ctxEl.appendChild(block);
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
