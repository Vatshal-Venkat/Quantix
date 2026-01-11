from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import (
    ParseResponse,
    SolveResponse,
    FeedbackRequest
)

from app.agents.parser_agent import parse_problem
from app.agents.intent_router import route_intent
from app.agents.solver_agent import solve_problem
from app.agents.verifier_agent import verify_solution
from app.agents.explainer_agent import explain_solution

from app.utils.ocr import extract_text_from_image
from app.utils.asr import transcribe_audio
from app.utils.confidence import assess_confidence
from app.hitl.handler import hitl_required
from app.memory.memory_store import store_interaction

app = FastAPI(title="Multimodal Math Mentor")

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
# 1. Parse input (Text / Image / Audio)
# ─────────────────────────────────────────────
@app.post("/parse", response_model=ParseResponse)
async def parse_input(
    input_type: str = Form(...),
    text: str = Form(None),
    file: UploadFile = File(None)
):
    raw_text = ""

    if input_type == "text":
        raw_text = text

    elif input_type == "image":
        raw_text = extract_text_from_image(await file.read())

    elif input_type == "audio":
        raw_text = transcribe_audio(await file.read())

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
# 2. Solve problem (RAG + Agents)
# ─────────────────────────────────────────────
@app.post("/solve", response_model=SolveResponse)
def solve(parsed_problem: dict):
    route = route_intent(parsed_problem)

    solution = solve_problem(parsed_problem, route)

    verification = verify_solution(parsed_problem, solution)

    explanation = explain_solution(parsed_problem, solution)

    return SolveResponse(
        solution=solution,
        explanation=explanation,
        verification=verification
    )


# ─────────────────────────────────────────────
# 3. Human feedback (HITL + Memory)
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
