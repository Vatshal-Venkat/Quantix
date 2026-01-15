from app.agents.gemini_client import get_gemini_model

SYSTEM_PROMPT = """
You are a fallback mathematics solver.

STRICT RULES:
- You are used ONLY when no answer exists in the knowledge base.
- Do NOT claim the problem is from any exam or PYQ.
- Do NOT hallucinate known results.
- If unsure, say you are unsure.
- Keep the final answer concise and factual.
"""

def solve_with_gemini(problem_text: str) -> dict:
    model = get_gemini_model()

    prompt = f"""
Solve the following problem carefully.

Problem:
{problem_text}

Instructions:
- If the solution is uncertain, state that clearly.
- Return ONLY the final answer in the first line.
"""

    response = model.generate_content(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    text = response.text.strip()

    first_line = text.splitlines()[0] if text else "Unable to determine the answer."

    return {
        "final_answer": {
            "text": first_line,
            "latex": ""
        },
        "used_llm_fallback": True
    }
