import re

OPERATIONS = {
    "gradient": "gradient",
    "jacobian": "jacobian",
    "hessian": "hessian",
    "differentiate": "derivative",
    "derivative": "derivative",
    "d/d": "derivative",
    "maximum": "optimization",
    "minimum": "optimization",
    "max": "optimization",
    "min": "optimization",
    "solve": "system"
}

TOPICS = {
    "gradient": "calculus",
    "derivative": "calculus",
    "jacobian": "linear_algebra",
    "hessian": "calculus",
    "limit": "calculus",
    "integral": "calculus",
    "system": "algebra",
    "optimization": "calculus"
}


def _normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\r", " ")
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def _split_into_subproblems(text: str) -> list[str]:
    """
    Splits multi-question input into atomic math problems.
    """
    parts = re.split(r"\n|\. (?=[A-Z]|find|solve|max|min)", text)
    return [p.strip() for p in parts if len(p.strip()) > 3]


def _detect_operation(text: str):
    text_l = text.lower()
    for key, op in OPERATIONS.items():
        if key in text_l:
            return op
    return None


def parse_problem(raw_text: str) -> dict:
    clean_text = _normalize_text(raw_text)
    subproblems = _split_into_subproblems(clean_text)

    parsed_items = []

    for sub in subproblems:
        operation = _detect_operation(sub)
        topic = TOPICS.get(operation, "unknown")

        variables = sorted(set(re.findall(r"[a-zA-Z]", sub)))

        parsed_items.append({
            "problem_text": sub,
            "operation": operation,
            "topic": topic,
            "variables": variables,
            "needs_clarification": False,
            "parser_metadata": {
                "auto_detected": operation is not None
            }
        })

    return {
        "original_text": clean_text,
        "subproblems": parsed_items
    }
