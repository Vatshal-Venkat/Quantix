let parsedProblem = null;
let solvedResult = null;

document.getElementById("inputType").addEventListener("change", (e) => {
  const type = e.target.value;
  document.getElementById("textInput").style.display = type === "text" ? "block" : "none";
  document.getElementById("fileInput").style.display = type !== "text" ? "block" : "none";
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
      alert("Please upload a file");
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
    JSON.stringify(data, null, 2);
}

async function solveProblem() {
  if (!parsedProblem) {
    alert("Parse the problem first");
    return;
  }

  const res = await fetch("/solve", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(parsedProblem)
  });

  const data = await res.json();
  solvedResult = data;

  document.getElementById("solutionOutput").textContent =
    JSON.stringify(data, null, 2);
}

async function sendFeedback(type) {
  if (!parsedProblem || !solvedResult) {
    alert("Nothing to give feedback on");
    return;
  }

  await fetch("/feedback", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      problem: parsedProblem,
      solution: solvedResult,
      feedback: type
    })
  });

  alert("Feedback submitted");
}
