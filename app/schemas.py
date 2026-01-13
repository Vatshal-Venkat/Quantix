from pydantic import BaseModel
from typing import Any, Optional, Dict, List


class ParseResponse(BaseModel):
    raw_text: str
    parsed_problem: dict
    confidence: str
    needs_hitl: bool


class AnswerSchema(BaseModel):
    text: str
    latex: str


class SolveResponse(BaseModel):
    final_answer: AnswerSchema
    steps: List[str]
    explanation: str
    used_context: List[str]
    used_memory: bool


class FeedbackRequest(BaseModel):
    problem: dict
    solution: Any
    feedback: str          # "correct" or "incorrect"
    correction: Optional[str] = None
