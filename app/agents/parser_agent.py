import re

OPERATIONS = {
    "gradient": "gradient",
    "jacobian": "jacobian",
    "hessian": "hessian",
    "differentiate": "derivative",
    "derivative": "derivative",
    "d/d": "derivative"
}

TOPICS = {
    "gradient": "calculus",
    "derivative": "calculus",
    "jacobian": "linear_algebra",
    "hessian": "calculus",
    "integral": "calculus",
    "limit": "calculus"
}

def parse_problem(raw_text: str) -> dict:
    text = raw_text.strip().lower()

    needs_clarification = len(text) < 10

    topic = "unknown"
    operation = None

    for key, value in TOPICS.items():
        if key in text:
            topic = value
            break

    for key, value in OPERATIONS.items():
        if key in text:
            operation = value
            break

    variables = sorted(set(re.findall(r"[a-zA-Z]", text)))

    return {
        "problem_text": raw_text.strip(),
        "topic": topic,
        "operation": operation,
        "variables": variables,
        "constraints": [],
        "needs_clarification": needs_clarification,
        "parser_metadata": {
            "confidence": "low" if needs_clarification else "high",
            "auto_detected": operation is not None
        }
    }
