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
    return {"text": text, "latex": latex}


def _supporting_context(title: str, paragraphs: list[str]):
    return {
        "title": title,
        "paragraphs": paragraphs
    }


# ─────────────────────────────────────────────
# Main solver
# ─────────────────────────────────────────────

def solve_problem(parsed_problem: dict, route: str) -> dict:

    if not isinstance(parsed_problem, dict):
        return {
            "final_answer": _answer("Invalid input format.", ""),
            "supporting_context": None,
            "used_context": [],
            "used_memory": False,
            "parser": None,
            "used_llm_fallback": False
        }

    problem_text = parsed_problem.get("problem_text", "").strip()

    if not problem_text:
        return {
            "final_answer": _answer("No problem provided.", ""),
            "supporting_context": None,
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
            "supporting_context": memory_match.get("supporting_context"),
            "used_context": ["memory"],
            "used_memory": True,
            "parser": parsed_problem,
            "used_llm_fallback": False
        }

    try:
        # ───────── DERIVATIVE
        if route == "quant_derivative":
            expr = _extract_rhs_expression(text)
            var = _first_symbol(expr)
            result = sp.simplify(sp.diff(expr, var))

            return {
                "final_answer": _answer(str(result), sp.latex(result)),
                "supporting_context": _supporting_context(
                    "How the derivative was computed",
                    [
                        "The given expression is treated as a function of a single variable.",
                        f"The derivative is taken with respect to {var}, holding other terms constant.",
                        "Symbolic differentiation rules are applied and the result is simplified."
                    ]
                ),
                "used_context": [],
                "used_memory": False,
                "parser": parsed_problem,
                "used_llm_fallback": False
            }

        # ───────── GRADIENT
        if route == "quant_gradient":
            expr = _extract_rhs_expression(text)
            vars_ = sorted(expr.free_symbols, key=lambda s: s.name)
            grad = [sp.simplify(sp.diff(expr, v)) for v in vars_]

            if len(grad) == 1:
                return {
                    "final_answer": _answer(str(grad[0]), sp.latex(grad[0])),
                    "supporting_context": _supporting_context(
                        "How the derivative was computed",
                        [
                            "Only one variable is present in the function.",
                            "The gradient reduces to a single partial derivative.",
                            "The expression is differentiated symbolically."
                        ]
                    ),
                    "used_context": [],
                    "used_memory": False,
                    "parser": parsed_problem,
                    "used_llm_fallback": False
                }

            grad_vec = sp.Matrix(grad)

            return {
                "final_answer": _answer(
                    f"[{', '.join(map(str, grad))}]",
                    sp.latex(grad_vec)
                ),
                "supporting_context": _supporting_context(
                    "How the gradient was computed",
                    [
                        "The function is interpreted as a scalar field of multiple variables.",
                        "The gradient is defined as the vector of partial derivatives with respect to each variable.",
                        "Each partial derivative measures the rate of change along one coordinate direction.",
                        "The resulting vector points in the direction of maximum increase of the function."
                    ]
                ),
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
                "supporting_context": _supporting_context(
                    "How the Jacobian was constructed",
                    [
                        "Each function is treated as a component of a vector-valued function.",
                        "Partial derivatives are computed with respect to each variable.",
                        "These derivatives are arranged into a matrix form called the Jacobian."
                    ]
                ),
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
                "supporting_context": _supporting_context(
                    "How the Hessian was constructed",
                    [
                        "Second-order partial derivatives are computed for all variable pairs.",
                        "These derivatives capture curvature information of the function.",
                        "They are assembled into a symmetric matrix known as the Hessian."
                    ]
                ),
                "used_context": [],
                "used_memory": False,
                "parser": parsed_problem,
                "used_llm_fallback": False
            }

        return {
            "final_answer": _answer("Unsupported symbolic operation.", ""),
            "supporting_context": None,
            "used_context": [],
            "used_memory": False,
            "parser": parsed_problem,
            "used_llm_fallback": False
        }

    except Exception as e:
        return {
            "final_answer": _answer("Symbolic solver failed.", ""),
            "supporting_context": _supporting_context(
                "Why the solver failed",
                [str(e)]
            ),
            "used_context": [],
            "used_memory": False,
            "parser": parsed_problem,
            "used_llm_fallback": False
        }
