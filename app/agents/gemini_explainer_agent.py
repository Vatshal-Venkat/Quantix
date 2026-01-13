from app.agents.gemini_client import get_gemini_model

SYSTEM_PROMPT = """
You explain math solutions.

Rules:
- Do NOT recompute.
- Do NOT change answers.
- Explain the given steps clearly.
- Be concise and educational.
"""

def explain_with_gemini(problem_text: str, final_answer: str, steps: list[str]) -> str:
    if not steps:
        return "Explanation unavailable."

    model = get_gemini_model()

    prompt = f"""
Problem:
{problem_text}

Final Answer:
{final_answer}

Steps:
{steps}

Explain the reasoning behind these steps.
"""

    response = model.generate_content(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return response.text.strip()
