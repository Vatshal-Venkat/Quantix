from app.agents.gemini_client import get_gemini_model

SYSTEM_PROMPT = """
You are a mathematics solver.

Rules:
- Solve the problem step by step.
- Use standard mathematical notation.
- Be precise and correct.
- If unsure, state assumptions clearly.
"""

def solve_with_gemini(problem_text: str) -> dict:
    model = get_gemini_model()

    prompt = f"""
Solve the following mathematical problem.

Problem:
{problem_text}

Return:
1. Final answer
2. Step-by-step solution
"""

    response = model.generate_content(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    text = response.text.strip()

    return {
        "final_answer": text.splitlines()[0],
        "steps": text.splitlines()[1:],
        "used_llm_fallback": True
    }
