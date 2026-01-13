let parsedProblem = null;
let solvedResult = null;

document.getElementById("inputType").addEventListener("change", (e) => {
  const type = e.target.value;
  document.getElementById("textInput").style.display =
    type === "text" ? "block" : "none";
  document.getElementById("fileInput").style.display =
    type !== "text" ? "block" : "none";
});

async function parseInput() {
  const inputType = document.getElementById("inputType").value;
  const text = document.getElementById("textInput").value;
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

  const res = await fetch("/parse", { method: "POST", body: formData });
  const data = await res.json();

  parsedProblem = data.parsed_problem;
  document.getElementById("parsedOutput").textContent =
    JSON.stringify(parsedProblem, null, 2);
}

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

  // ───── Final Answer (Text) ─────
  document.getElementById("answerText").textContent =
    data.final_answer?.text || "";

  // ───── Final Answer (LaTeX) ─────
  const latexEl = document.getElementById("answerLatex");
  latexEl.innerHTML = data.final_answer?.latex
    ? `$$${data.final_answer.latex}$$`
    : "";

  // ───── Supporting Context ─────
  const ctxEl = document.getElementById("supportingContext");
  ctxEl.innerHTML = "";

  if (data.supporting_context) {
    const title = document.createElement("h3");
    title.textContent = data.supporting_context.title;
    ctxEl.appendChild(title);

    (data.supporting_context.paragraphs || []).forEach(p => {
      const para = document.createElement("p");
      para.textContent = p;
      ctxEl.appendChild(para);
    });
  }

  // ───── System Info ─────
  document.getElementById("systemInfo").textContent =
    `Memory used: ${data.used_memory}`;

  // Re-render MathJax
  if (window.MathJax && data.final_answer?.latex) {
    MathJax.typesetPromise();
  }
}

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
