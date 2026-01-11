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

  // ───── Final Answer (ROBUST) ─────
  const finalAnswerEl = document.getElementById("finalAnswer");

  if (data.final_answer && data.final_answer.trim() !== "") {
    finalAnswerEl.textContent = data.final_answer;
  } else if (data.explanation) {
    const line = data.explanation
      .split("\n")
      .find(l => l.toLowerCase().startsWith("final answer"));
    finalAnswerEl.textContent = line
      ? line.replace("Final Answer:", "").trim()
      : "Answer generated. See explanation below.";
  } else {
    finalAnswerEl.textContent = "Answer generated.";
  }

  // ───── Steps ─────
  const stepsEl = document.getElementById("steps");
  stepsEl.innerHTML = "";
  (data.steps || []).forEach(step => {
    const li = document.createElement("li");
    li.textContent = step;
    stepsEl.appendChild(li);
  });

  // ───── Sources ─────
  const sourcesEl = document.getElementById("sources");
  sourcesEl.innerHTML = "";
  (data.used_context || []).forEach(src => {
    const li = document.createElement("li");
    li.textContent = src;
    sourcesEl.appendChild(li);
  });

  // ───── System Info ─────
  document.getElementById("systemInfo").textContent =
    `Memory used: ${data.used_memory}`;
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
