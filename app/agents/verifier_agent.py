def verify_solution(parsed_problem: dict, solution: dict) -> dict:
    # Simple heuristic verifier
    answer = solution.get("final_answer", "")

    if not answer or "placeholder" in answer.lower():
        return {
            "is_correct": False,
            "confidence": 0.4,
            "issues": ["Answer seems incomplete"]
        }

    return {
        "is_correct": True,
        "confidence": 0.9,
        "issues": []
    }
