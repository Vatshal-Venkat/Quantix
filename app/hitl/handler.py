def hitl_required(confidence: str, parsed_problem: dict) -> bool:
    if confidence == "low":
        return True
    if parsed_problem.get("needs_clarification"):
        return True
    return False
