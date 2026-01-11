def explain_solution(parsed_problem: dict, solution: dict) -> str:
    explanation = []

    # 🔒 Defensive access (prevents crashes)
    problem_text = parsed_problem.get(
        "problem_text", "Problem statement not available"
    )

    explanation.append(f"Problem: {problem_text}\n")

    steps = solution.get("steps", [])
    for idx, step in enumerate(steps, start=1):
        explanation.append(f"Step {idx}: {step}")

    explanation.append(
        f"\nFinal Answer: {solution.get('final_answer', 'N/A')}"
    )

    return "\n".join(explanation)
