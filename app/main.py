# main.py (UPDATED — MULTI-PROBLEM SAFE + EXPLAINER)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from fastapi import FastAPI, UploadFile, File, Form, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import os
import re

from app.schemas import ParseResponse, FeedbackRequest
from app.agents.parser_agent import parse_problem
from app.agents.solver_agent import solve_problem
from app.agents.gemini_explainer_agent import explain_with_gemini
from app.utils.ocr import extract_text_from_image
from app.utils.asr import transcribe_audio
from app.utils.confidence import assess_confidence
from app.hitl.handler import hitl_required
from app.memory.memory_store import store_interaction

# ─────────────────────────────────────────────
# App init
# ─────────────────────────────────────────────
app = FastAPI(title="Quantix Mathematician")

# ─────────────────────────────────────────────
# Middleware
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Static frontend
# ─────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def serve_ui():
    with open("app/static/index.html", "r", encoding="utf-8") as f:
        return f.read()


# ─────────────────────────────────────────────
# Parse input
# ─────────────────────────────────────────────
@app.post("/parse", response_model=ParseResponse)
async def parse_input(
    input_type: str = Form(...),
    text: str = Form(None),
    file: UploadFile = File(None)
):
    if input_type == "text":
        raw_text = text or ""
    elif input_type == "image" and file:
        raw_text = extract_text_from_image(await file.read())
    elif input_type == "audio" and file:
        raw_text = transcribe_audio(await file.read())
    else:
        raw_text = ""

    # Normalize input aggressively (CRITICAL)
    raw_text = raw_text.replace("\r", " ")
    raw_text = raw_text.replace("\n", " ")
    raw_text = re.sub(r"\s+", " ", raw_text).strip()

    confidence = assess_confidence(raw_text)
    parsed = parse_problem(raw_text)
    needs_hitl = hitl_required(confidence, parsed)

    return ParseResponse(
        raw_text=raw_text,
        parsed_problem=parsed,
        confidence=confidence,
        needs_hitl=needs_hitl
    )


# ─────────────────────────────────────────────
# Solve (MULTI-PROBLEM + EXPLAINER)
# ─────────────────────────────────────────────
@app.post("/solve")
async def solve(parsed_problem: dict = Body(...)):
    try:
        if not isinstance(parsed_problem, dict):
            raise ValueError("Invalid request body")

        solution = solve_problem(parsed_problem)

        # ─────────────────────────────────────
        # EXPLAINER (NON-DESTRUCTIVE)
        # ─────────────────────────────────────
        # Adds explanation ONLY if missing
        # or appends clarification if already present
        if os.getenv("GEMINI_API_KEY"):
            for item in solution.get("results", []):
                if not item.get("explanation"):
                    try:
                        item["explanation"] = explain_with_gemini(
                            item.get("question", ""),
                            item.get("final_answer", {}).get("text", "")
                        )
                        item["source"]["explanation"] = "gemini_explainer"
                    except Exception:
                        # Never fail solve because of explainer
                        pass

        return JSONResponse(
            status_code=200,
            content=solution
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Solve endpoint failed",
                "details": str(e)
            }
        )


# ─────────────────────────────────────────────
# Feedback
# ─────────────────────────────────────────────
@app.post("/feedback")
def feedback(request: FeedbackRequest):
    store_interaction(
        problem=request.problem,
        solution=request.solution,
        feedback=request.feedback,
        correction=request.correction
    )
    return JSONResponse({"status": "stored"})
