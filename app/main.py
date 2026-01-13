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

from app.schemas import ParseResponse, FeedbackRequest
from app.agents.parser_agent import parse_problem
from app.agents.intent_router import route_intent
from app.agents.solver_agent import solve_problem
from app.agents.gemini_explainer_agent import explain_with_gemini
from app.utils.ocr import extract_text_from_image
from app.utils.asr import transcribe_audio
from app.utils.confidence import assess_confidence
from app.hitl.handler import hitl_required
from app.memory.memory_store import store_interaction

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
# Solve (FINAL FIX)
# ─────────────────────────────────────────────
@app.post("/solve")
async def solve(parsed_problem: dict = Body(...)):
    try:
        if not isinstance(parsed_problem, dict):
            raise ValueError("Invalid request body: expected JSON object")

        route = route_intent(parsed_problem)
        solution = solve_problem(parsed_problem, route)

        # 🔒 Gemini explainer is OPTIONAL
        if os.getenv("GEMINI_API_KEY"):
            explanation = explain_with_gemini(
                parsed_problem.get("problem_text", ""),
                solution.get("final_answer", ""),
                solution.get("steps", [])
            )
        else:
            explanation = "Explanation unavailable (Gemini not configured)."

        return {
            "final_answer": solution.get("final_answer", "Solution generated."),
            "steps": solution.get("steps", []),
            "explanation": explanation,
            "used_context": solution.get("used_context", []),
            "used_memory": solution.get("used_memory", False)
        }

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
