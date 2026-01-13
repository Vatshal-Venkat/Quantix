from app.rag.retriever import retrieve_context
from app.memory.similarity import find_similar_problem
from app.agents.gemini_solver_agent import solve_with_gemini  # kept, NOT auto-used

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
    expr_text = expr_text.replace("^", "**")
    return parse_expr(expr_text, transformations=TRANSFORMATIONS)


def _extract_rhs_expression(text: str):
    """
    Extract RHS after '='
    Handles implicit multiplication safely.
    """
    match = re.search(r"=\s*(.+)", text)
    if not match:
        raise ValueError("No '=' found in expression")
    return _parse_expr(match.group(1))


def _first_symbol(expr):
    vars_ = sorted(expr.free_symbols, key=lambda s: s.name)
    if not vars_:
        raise ValueError("No variable found in expression")
    return vars_[0]


def _answer(text: str, latex: str):
    return {
        "text": text,
        "latex": latex
    }


# ─────────────────────────────────────────────
# Main solver
# ─────────────────────────────────────────────

def solve_problem(parsed_problem: dict, route: str) -> dict:
    """
    FULL SYMBOLIC MATH SOLVER (ROUTE-DRIVEN)

    ✔ Deterministic SymPy
    ✔ Multi-variable support
    ✔ Plain text + LaTeX output
    ✖ No automatic LLM fallback
    """

    # ───────────────── SAFE INPUT
    if not isinstance(parsed_problem, dict):
        return {
            "final_answer": _answer("Invalid input format.", ""),
            "steps": [],
            "used_context": [],
            "used_memory": False,
            "parser": None,
            "used_llm_fallback": False
        }

    problem_text = parsed_problem.get("problem_text", "").strip()

    if not problem_text:
        return {
            "final_answer": _answer("No problem provided.", ""),
            "steps": [],
            "used_context": [],
            "used_memory": False,
            "parser": parsed_problem,
            "used_llm_fallback": False
        }

    text = problem_text.lower()

    # ───────────────── MEMORY CHECK
    try:
        memory_match = find_similar_problem(problem_text)
    except Exception:
        memory_match = None

    if memory_match:
        return {
            "final_answer": memory_match.get("final_answer"),
            "steps": memory_match.get("solution_steps") or [],
            "used_context": ["memory"],
            "used_memory": True,
            "parser": parsed_problem,
            "used_llm_fallback": False
        }

    # ───────────────── SYMBOLIC SOLVING
    try:
        # ───────── DERIVATIVE
        if route == "quant_derivative":
            expr = _extract_rhs_expression(text)
            var = _first_symbol(expr)
            result = sp.simplify(sp.diff(expr, var))

            return {
                "final_answer": _answer(str(result), sp.latex(result)),
                "steps": [
                    f"Differentiated with respect to {var}"
                ],
                "used_context": [],
                "used_memory": False,
                "parser": parsed_problem,
                "used_llm_fallback": False
            }

        # ───────── GRADIENT (FIXED UX)
        if route == "quant_gradient":
            expr = _extract_rhs_expression(text)
            vars_ = sorted(expr.free_symbols, key=lambda s: s.name)

            grad = [sp.simplify(sp.diff(expr, v)) for v in vars_]

            # SINGLE VARIABLE → scalar derivative
            if len(grad) == 1:
                return {
                    "final_answer": _answer(
                        str(grad[0]),
                        sp.latex(grad[0])
                    ),
                    "steps": [
                        f"Computed derivative with respect to {vars_[0]}"
                    ],
                    "used_context": [],
                    "used_memory": False,
                    "parser": parsed_problem,
                    "used_llm_fallback": False
                }

            # MULTI-VARIABLE → gradient vector
            grad_vec = sp.Matrix(grad)

            return {
                "final_answer": _answer(
                    f"[{', '.join(map(str, grad))}]",
                    sp.latex(grad_vec)
                ),
                "steps": [
                    f"Computed gradient with respect to {', '.join(map(str, vars_))}"
                ],
                "used_context": [],
                "used_memory": False,
                "parser": parsed_problem,
                "used_llm_fallback": False
            }

        # ───────── JACOBIAN
        if route == "quant_jacobian":
            matches = re.findall(r"\[(.*?)\]", text)
            if not matches:
                raise ValueError("Jacobian requires [f1, f2, ...] format")

            funcs = [_parse_expr(f.strip()) for f in matches[0].split(",")]
            vars_ = sorted(
                set().union(*[f.free_symbols for f in funcs]),
                key=lambda s: s.name
            )

            J = sp.Matrix(funcs).jacobian(vars_)

            return {
                "final_answer": _answer("Jacobian computed", sp.latex(J)),
                "steps": ["Constructed Jacobian matrix"],
                "used_context": [],
                "used_memory": False,
                "parser": parsed_problem,
                "used_llm_fallback": False
            }

        # ───────── HESSIAN
        if route == "quant_hessian":
            expr = _extract_rhs_expression(text)
            vars_ = sorted(expr.free_symbols, key=lambda s: s.name)
            H = sp.hessian(expr, vars_)

            return {
                "final_answer": _answer("Hessian computed", sp.latex(H)),
                "steps": ["Constructed Hessian matrix"],
                "used_context": [],
                "used_memory": False,
                "parser": parsed_problem,
                "used_llm_fallback": False
            }

        # ───────── FALLBACK
        return {
            "final_answer": _answer("Unsupported symbolic operation.", ""),
            "steps": [],
            "used_context": [],
            "used_memory": False,
            "parser": parsed_problem,
            "used_llm_fallback": False
        }

    # ───────────────── HARD SAFE FAILURE
    except Exception as e:
        return {
            "final_answer": _answer("Symbolic solver failed.", ""),
            "steps": [str(e)],
            "used_context": [],
            "used_memory": False,
            "parser": parsed_problem,
            "used_llm_fallback": False
        }
