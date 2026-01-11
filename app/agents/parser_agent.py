import re

TOPICS = {
    "derivative": "calculus",
    "integral": "calculus",
    "limit": "calculus",
    "probability": "probability",
    "matrix": "linear_algebra",
    "determinant": "linear_algebra"
}

def parse_problem(raw_text: str) -> dict:
    text = raw_text.strip()

    needs_clarification = len(text) < 10

    topic = "unknown"
    subtopic = None

    for key, value in TOPICS.items():
        if key in text.lower():
            topic = value
            subtopic = key
            break

    variables = re.findall(r"[a-zA-Z]", text)

    return {
        "problem_text": text,
        "topic": topic,
        "subtopic": subtopic,
        "variables": list(set(variables)),
        "constraints": [],
        "needs_clarification": needs_clarification
    }
