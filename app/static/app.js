let parsedProblem = null;
let solvedResult = null;

/* =========================================================
   INPUT MODE TOGGLING
   ========================================================= */
document.getElementById("inputType").addEventListener("change", (e) => {
  const type = e.target.value;

  const textInput = document.getElementById("textInput");
  const fileInput = document.getElementById("fileInput");
  const audioInput = document.getElementById("audioInput");

  textInput.style.display = type === "text" ? "block" : "none";
  fileInput.style.display = type === "image" ? "block" : "none";
  audioInput.style.display = type === "audio" ? "block" : "none";
});

/* =========================================================
   PARSE INPUT
   ========================================================= */
async function parseInput() {
  const inputType = document.getElementById("inputType").value;
  const formData = new FormData();
  formData.append("input_type", inputType);

  if (inputType === "text") {
    const text = document
      .getElementById("textInput")
      .value.replace(/\n+/g, " ")
      .replace(/\s+/g, " ")
      .trim();

    if (!text) {
      alert("Enter a problem");
      return;
    }

    formData.append("text", text);
  }

  else if (inputType === "audio") {
    const audioText = document.getElementById("audioText").value.trim();
    if (!audioText) {
      alert("Speak a problem first");
      return;
    }
    formData.append("text", audioText);
  }

  else {
    const fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) {
      alert("Upload an image");
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

/* =========================================================
   SOLVE
   ========================================================= */
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

  solvedResult = await res.json();
  renderResults(solvedResult);
}

/* Audio solve shortcut */
function solveFromAudio() {
  parseInput().then(solveProblem);
}

/* =========================================================
   RENDER RESULTS
   ========================================================= */
function renderResults(data) {
  const answerTextEl = document.getElementById("answerText");
  const answerLatexEl = document.getElementById("answerLatex");
  const ctxEl = document.getElementById("supportingContext");
  const sysInfoEl = document.getElementById("systemInfo");

  answerTextEl.innerHTML = "";
  answerLatexEl.innerHTML = "";
  ctxEl.innerHTML = "";
  sysInfoEl.textContent = "";

  if (!data.results || data.results.length === 0) {
    answerTextEl.textContent = "No results returned.";
    return;
  }

  sysInfoEl.textContent = `Total problems solved: ${data.total_problems}`;

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

  if (window.MathJax) {
    MathJax.typesetPromise();
  }
}

/* =========================================================
   FEEDBACK
   ========================================================= */
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

/* =========================================================
   SPEECH TO TEXT (AUDIO MODE)
   ========================================================= */
let recognition;
let listening = false;

const audioText = document.getElementById("audioText");
const micCircle = document.querySelector(".mic-circle");

/* --------- SPOKEN MATH → SYMBOLS --------- */
function normalizeMathSpeech(text) {
  let t = text.toLowerCase();

  let isDiff = false;
  let isIntegrate = false;
  let isLimit = false;
  let isSimplify = false;
  let isFactor = false;
  let isExpand = false;

  if (t.includes("derivative") || t.includes("differentiate")) {
    isDiff = true;
    t = t.replace(/derivative of|derivative|differentiate/gi, "");
  }

  if (t.includes("integrate") || t.includes("integral")) {
    isIntegrate = true;
    t = t.replace(/integrate|integral of|integral/gi, "");
  }

  if (t.includes("limit")) {
    isLimit = true;
    t = t.replace(/limit of|limit/gi, "");
  }

  if (t.includes("simplify")) {
    isSimplify = true;
    t = t.replace(/simplify/gi, "");
  }

  if (t.includes("factor")) {
    isFactor = true;
    t = t.replace(/factor/gi, "");
  }

  if (t.includes("expand")) {
    isExpand = true;
    t = t.replace(/expand/gi, "");
  }

  const replacements = {
    plus: "+",
    minus: "-",
    times: "*",
    into: "*",
    "divide by": "/",
    "divided by": "/",
    by: "/",
    equals: "=",
    "equal to": "=",
    square: "**2",
    cube: "**3",
    power: "**",
    "open bracket": "(",
    "close bracket": ")",
    "open parenthesis": "(",
    "close parenthesis": ")",
    sin: "sin",
    sine: "sin",
    cos: "cos",
    cosine: "cos",
    tan: "tan",
    tangent: "tan",
    log: "log",
    "natural log": "ln",
    "square root": "sqrt",
    zero: "0",
    one: "1",
    two: "2",
    three: "3",
    four: "4",
    five: "5",
  };

  for (const key in replacements) {
    const regex = new RegExp(`\\b${key}\\b`, "g");
    t = t.replace(regex, replacements[key]);
  }

  t = t.replace(/(\d)([a-z])/g, "$1*$2");
  t = t.replace(/([a-z])(\d)/g, "$1*$2");
  t = t.replace(/([a-z])\s+([a-z])/g, "$1*$2");
  t = t.replace(/\s+/g, "");

  if (isDiff) return `diff(${t})`;
  if (isIntegrate) return `integrate(${t})`;
  if (isSimplify) return `simplify(${t})`;
  if (isFactor) return `factor(${t})`;
  if (isExpand) return `expand(${t})`;

  return t;
}

/* --------- START / STOP MIC --------- */
function startVoice() {
  if (!("webkitSpeechRecognition" in window)) {
    alert("Speech recognition not supported");
    return;
  }

  if (!recognition) {
    recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = (event) => {
      let transcript = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      audioText.value = normalizeMathSpeech(transcript);
    };

    recognition.onend = () => {
      if (listening) recognition.start();
    };
  }

  if (!listening) {
    listening = true;
    micCircle.classList.add("listening");
    recognition.start();
  } else {
    stopVoice();
  }
}

function stopVoice() {
  listening = false;
  micCircle.classList.remove("listening");
  recognition.stop();
}

function resetAudio() {
  audioText.value = "";
  if (recognition && listening) recognition.stop();
  listening = false;
  micCircle.classList.remove("listening");
}

/* =========================================================
   FORCE CORRECT UI ON INITIAL LOAD (SAFE FIX)
   ========================================================= */
window.addEventListener("DOMContentLoaded", () => {
  document.getElementById("inputType").dispatchEvent(
    new Event("change")
  );
});
