def explain_solution(parsed_problem: dict, solution: dict) -> str:
    explanation = []
    explanation.append(f"Problem: {parsed_problem['problem_text']}\n")

    for idx, step in enumerate(solution.get("steps", []), start=1):
        explanation.append(f"Step {idx}: {step}")

    explanation.append(f"\nFinal Answer: {solution.get('final_answer')}")

    return "\n".join(explanation)
