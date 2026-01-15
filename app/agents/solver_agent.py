from app.rag.retriever import retrieve_context
from app.memory.similarity import find_similar_problem
from app.agents.gemini_solver_agent import solve_with_gemini  # fallback only

import sympy as sp
import re

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)

# ─────────────────────────────────────────────
# Parsing utilities
# ─────────────────────────────────────────────

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
)


def _parse_expr(expr_text: str):
    return parse_expr(expr_text.replace("^", "**"), transformations=TRANSFORMATIONS)


def _extract_rhs_expression(text: str):
    match = re.search(r"=\s*(.+)", text)
    if not match:
        raise ValueError("No '=' found in expression")
    return _parse_expr(match.group(1))


def _first_symbol(expr):
    vars_ = sorted(expr.free_symbols, key=lambda s: s.name)
    if not vars_:
        raise ValueError("No variable found")
    return vars_[0]


def _answer(text: str, latex: str = ""):
    return {"text": text, "latex": latex}


def _extract_doc_answer(results: list[dict]) -> str:
    if not results:
        return None
    return results[0].get("answer") or results[0].get("content")


# ─────────────────────────────────────────────
# SOLVE A SINGLE SUB-PROBLEM
# ─────────────────────────────────────────────

def _solve_single(subproblem: dict) -> dict:
    problem_text = subproblem["problem_text"]
    route = subproblem.get("route")

    # 1️⃣ DOC FIRST
    try:
        kb_results = retrieve_context(problem_text)
    except Exception:
        kb_results = []

    if kb_results:
        return {
            "question": problem_text,
            "final_answer": _answer(_extract_doc_answer(kb_results)),
            "source": "knowledge_base"
        }

    # 2️⃣ MEMORY
    try:
        memory_match = find_similar_problem(problem_text)
    except Exception:
        memory_match = None

    if memory_match:
        return {
            "question": problem_text,
            "final_answer": memory_match.get("final_answer"),
            "source": "memory"
        }

    text = problem_text.lower()

    # 3️⃣ SYMBOLIC SOLVERS
    try:
        # ───────── DERIVATIVE
        if route == "quant_derivative":
            expr = _extract_rhs_expression(text)
            var = _first_symbol(expr)
            d = sp.diff(expr, var)

            # Evaluate at a point if asked
            m = re.search(r"\((\-?\d+)\)", text)
            if m:
                d = d.subs(var, int(m.group(1)))

            return {
                "question": problem_text,
                "final_answer": _answer(str(d), sp.latex(d)),
                "source": "symbolic"
            }

        # ───────── SYSTEM OF EQUATIONS
        if route == "quant_system":
            eqs = re.findall(r"([a-zA-Z0-9+\-*/ ]+=+[a-zA-Z0-9+\-*/ ]+)", problem_text)
            sym_eqs = [sp.Eq(*map(_parse_expr, e.split("="))) for e in eqs]
            vars_ = sorted(
                set().union(*[e.free_symbols for e in sym_eqs]),
                key=lambda s: s.name
            )
            sol = sp.solve(sym_eqs, vars_, dict=True)

            return {
                "question": problem_text,
                "final_answer": _answer(str(sol)),
                "source": "symbolic"
            }

        # ───────── OPTIMIZATION
        if route == "quant_optimization":
            expr = _extract_rhs_expression(text)
            var = _first_symbol(expr)
            d = sp.diff(expr, var)
            critical = sp.solve(d, var)
            values = [expr.subs(var, c) for c in critical]

            result = max(values) if "max" in text else min(values)

            return {
                "question": problem_text,
                "final_answer": _answer(str(result)),
                "source": "symbolic"
            }

    except Exception:
        pass

    # 4️⃣ LLM FALLBACK
    llm = solve_with_gemini(problem_text)
    return {
        "question": problem_text,
        "final_answer": llm["final_answer"],
        "source": "llm"
    }


# ─────────────────────────────────────────────
# MAIN ENTRY — MULTI-PROBLEM EXECUTION
# ─────────────────────────────────────────────

def solve_problem(parsed_payload: dict) -> dict:
    results = []

    from app.agents.intent_router import route_intent

    for sub in parsed_payload.get("subproblems", []):
        sub["route"] = route_intent(sub)
        solved = _solve_single(sub)
        results.append(solved)

    return {
        "total_problems": len(results),
        "results": results
    }
