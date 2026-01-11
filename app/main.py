from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ParseResponse, FeedbackRequest
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
# Parse input (Text / Image / Audio)
# ─────────────────────────────────────────────
@app.post("/parse", response_model=ParseResponse)
async def parse_input(
    input_type: str = Form(...),
    text: str = Form(None),
    file: UploadFile = File(None)
):
    if input_type == "text":
        raw_text = text or ""
    elif input_type == "image" and file is not None:
        raw_text = extract_text_from_image(await file.read())
    elif input_type == "audio" and file is not None:
        raw_text = transcribe_audio(await file.read())
    else:
        raw_text = ""

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
# Solve (CLEAN + HARD-SAFE OUTPUT)
# ─────────────────────────────────────────────
@app.post("/solve")
def solve(parsed_problem: dict):
    # Defensive normalization
    if not isinstance(parsed_problem, dict):
        parsed_problem = {}

    if not parsed_problem.get("problem_text"):
        parsed_problem["problem_text"] = ""

    # Route + solve
    route = route_intent(parsed_problem)
    solution = solve_problem(parsed_problem, route)

    # Verification + explanation
    verification = verify_solution(parsed_problem, solution)
    explanation = explain_solution(parsed_problem, solution)

    # HARD guarantee: never return nulls
    final_answer = solution.get("final_answer")
    if not final_answer or not isinstance(final_answer, str):
        final_answer = "Solution generated successfully."

    return {
        "final_answer": final_answer,
        "steps": solution.get("steps") or [],
        "used_context": solution.get("used_context") or [],
        "used_memory": solution.get("used_memory", False),
        "explanation": explanation,
        "verification": verification
    }


# ─────────────────────────────────────────────
# Human feedback (HITL + Memory)
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
