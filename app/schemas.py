from pydantic import BaseModel
from typing import Any, Optional


class ParseResponse(BaseModel):
    raw_text: str
    parsed_problem: dict
    confidence: str
    needs_hitl: bool


class SolveResponse(BaseModel):
    solution: Any
    explanation: str
    verification: dict


class FeedbackRequest(BaseModel):
    problem: dict
    solution: Any
    feedback: str          # "correct" or "incorrect"
    correction: Optional[str] = None
