from app.rag.retriever import retrieve_context
from app.memory.similarity import find_similar_problem
from app.agents.gemini_solver_agent import solve_with_gemini  # kept, but NOT auto-used

import sympy as sp
import re

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)

# ─────────────────────────────────────────────
# Utility helpers
# ─────────────────────────────────────────────

def _first_symbol(expr):
    vars_ = sorted(expr.free_symbols, key=lambda s: s.name)
    if not vars_:
        raise ValueError("No variable found in expression")
    return vars_[0]


def _latex_steps(*lines):
    return [line for line in lines if line]


def _extract_rhs_expression(text: str):
    """
    Extract RHS of expression after '=' and
    correctly handle implicit multiplication.

    Example:
    'find the gradient of f(x) = 3x^3 - 5x + 7'
    → 3*x**3 - 5*x + 7
    """
    match = re.search(r"=\s*(.+)", text)
    if not match:
        raise ValueError("No '=' found in expression")

    expr_text = match.group(1)
    expr_text = expr_text.replace("^", "**")

    transformations = standard_transformations + (
        implicit_multiplication_application,
    )

    return parse_expr(expr_text, transformations=transformations)


# ─────────────────────────────────────────────
# Main solver
# ─────────────────────────────────────────────

def solve_problem(parsed_problem: dict, route: str) -> dict:
    """
    FULL SYMBOLIC MATH SOLVER (QUANT-FIRST)

    ✔ Deterministic SymPy
    ✖ No automatic LLM fallback
    """

    # ─────────────────────────────────────────────
    # SAFE INPUT EXTRACTION
    # ─────────────────────────────────────────────
    if not isinstance(parsed_problem, dict):
        return {
            "final_answer": "Invalid input format.",
            "steps": [],
            "used_context": [],
            "used_memory": False,
            "parser": None,
            "used_llm_fallback": False
        }

    problem_text = parsed_problem.get("problem_text", "").strip()

    if not problem_text:
        return {
            "final_answer": "No problem provided.",
            "steps": [],
            "used_context": [],
            "used_memory": False,
            "parser": parsed_problem,
            "used_llm_fallback": False
        }

    text = problem_text.lower()

    # ─────────────────────────────────────────────
    # MEMORY CHECK
    # ─────────────────────────────────────────────
    try:
        memory_match = find_similar_problem(problem_text)
    except Exception:
        memory_match = None

    if memory_match:
        return {
            "final_answer": memory_match.get("final_answer", "Memory-based solution"),
            "steps": memory_match.get("solution_steps") or [],
            "used_context": ["memory"],
            "used_memory": True,
            "parser": parsed_problem,
            "used_llm_fallback": False
        }

    # ─────────────────────────────────────────────
    # SYMBOLIC SOLVING (PRIMARY & ONLY PATH)
    # ─────────────────────────────────────────────
    try:
        steps = []
        final_answer = ""

        # ───────── PARTIAL DERIVATIVE d/dx(f)
        d_match = re.search(r"d/d([a-z])\((.*?)\)", text)
        if d_match:
            var_name, expr_text = d_match.groups()
            x, y, z = sp.symbols("x y z")
            var_map = {"x": x, "y": y, "z": z}

            if var_name not in var_map:
                raise ValueError("Unsupported differentiation variable")

            var = var_map[var_name]

            transformations = standard_transformations + (
                implicit_multiplication_application,
            )

            expr = parse_expr(expr_text.replace("^", "**"), transformations=transformations)
            result = sp.simplify(sp.diff(expr, var))

            steps = _latex_steps(
                f"Original expression: $${sp.latex(expr)}$$",
                f"Differentiate w.r.t. $${sp.latex(var)}$$",
                f"Result: $${sp.latex(result)}$$"
            )
            final_answer = sp.latex(result)

        # ───────── STANDARD DERIVATIVE
        elif any(k in text for k in ["differentiate", "derivative of", "find the derivative"]):
            expr = _extract_rhs_expression(text)
            var = _first_symbol(expr)
            result = sp.simplify(sp.diff(expr, var))

            steps = _latex_steps(
                f"Expression: $${sp.latex(expr)}$$",
                f"Differentiate w.r.t. $${sp.latex(var)}$$",
                f"Result: $${sp.latex(result)}$$"
            )
            final_answer = sp.latex(result)

        # ───────── GRADIENT
        elif "gradient" in text:
            expr = _extract_rhs_expression(text)
            vars_ = sorted(expr.free_symbols, key=lambda s: s.name)

            grad = [sp.diff(expr, v) for v in vars_]
            result = sp.Matrix(grad)

            steps = _latex_steps(
                f"Function: $${sp.latex(expr)}$$",
                f"Variables: $${', '.join(map(sp.latex, vars_))}$$",
                f"Gradient: $${sp.latex(result)}$$"
            )
            final_answer = sp.latex(result)

        # ───────── JACOBIAN
        elif "jacobian" in text:
            matches = re.findall(r"\[(.*?)\]", text)
            if not matches:
                raise ValueError("Jacobian requires [f1, f2, ...] format")

            funcs = [
                parse_expr(f.strip().replace("^", "**"),
                           transformations=standard_transformations + (implicit_multiplication_application,))
                for f in matches[0].split(",")
            ]

            vars_ = sorted(
                set().union(*[f.free_symbols for f in funcs]),
                key=lambda s: s.name
            )

            J = sp.Matrix(funcs).jacobian(vars_)

            steps = _latex_steps(
                f"Functions: $${sp.latex(sp.Matrix(funcs))}$$",
                f"Variables: $${', '.join(map(sp.latex, vars_))}$$",
                f"Jacobian: $${sp.latex(J)}$$"
            )
            final_answer = sp.latex(J)

        # ───────── HESSIAN
        elif "hessian" in text:
            expr = _extract_rhs_expression(text)
            vars_ = sorted(expr.free_symbols, key=lambda s: s.name)

            H = sp.hessian(expr, vars_)

            steps = _latex_steps(
                f"Function: $${sp.latex(expr)}$$",
                f"Variables: $${', '.join(map(sp.latex, vars_))}$$",
                f"Hessian: $${sp.latex(H)}$$"
            )
            final_answer = sp.latex(H)

        else:
            raise ValueError("Unsupported symbolic operation")

        # ─────────────────────────────────────────────
        # CONTEXT RETRIEVAL
        # ─────────────────────────────────────────────
        try:
            retrieved_context = retrieve_context(problem_text, top_k=3) or []
            used_context = list(
                {ctx.get("source") for ctx in retrieved_context if isinstance(ctx, dict)}
            )
        except Exception:
            used_context = []

        return {
            "final_answer": final_answer,
            "steps": steps,
            "used_context": used_context,
            "used_memory": False,
            "parser": parsed_problem,
            "used_llm_fallback": False
        }

    # ─────────────────────────────────────────────
    # HARD SAFE FAILURE (NO GEMINI)
    # ─────────────────────────────────────────────
    except Exception as e:
        return {
            "final_answer": "Symbolic solver failed.",
            "steps": [str(e)],
            "used_context": [],
            "used_memory": False,
            "parser": parsed_problem,
            "used_llm_fallback": False
        }
