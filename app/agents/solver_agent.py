from app.rag.retriever import retrieve_context
from app.memory.similarity import find_similar_problem

import sympy as sp
import re


def solve_problem(parsed_problem: dict, route: str) -> dict:
    """
    FULL SYMBOLIC MATH SOLVER (ROUTE-AGNOSTIC)

    Supports:
    - Derivatives (single & partial)
    - Gradients
    - Jacobians
    - Hessians
    - Definite & Indefinite Integrals
    - Limits
    - Taylor Series
    - Step-by-step symbolic explanation
    - LaTeX output
    """

    problem_text = (
        parsed_problem.get("problem_text", "")
        if isinstance(parsed_problem, dict)
        else ""
    )

    text = problem_text.lower()

    # ─────────────────────────────────────────────
    # 1. MEMORY CHECK
    # ─────────────────────────────────────────────
    memory_match = find_similar_problem(problem_text)
    if memory_match:
        return {
            "final_answer": memory_match.get("final_answer", "Memory-based solution"),
            "steps": memory_match.get("solution_steps") or [],
            "used_context": ["memory"],
            "used_memory": True
        }

    final_answer = ""
    steps = []

    try:
        # ─────────────────────────────────────────────
        # PARTIAL DERIVATIVE: d/dz(...)
        # ─────────────────────────────────────────────
        d_match = re.search(r"d/d([a-z])\((.*?)\)", text)
        if d_match:
            var_name = d_match.group(1)
            expr_text = d_match.group(2)

            x, y, z = sp.symbols("x y z")
            var_map = {"x": x, "y": y, "z": z}
            var = var_map[var_name]

            expr = sp.sympify(expr_text)
            derivative = sp.diff(expr, var)
            simplified = sp.simplify(derivative)

            steps = [
                f"Original expression: $${sp.latex(expr)}$$",
                f"Differentiate with respect to $${sp.latex(var)}$$",
                f"Partial derivative: $${sp.latex(derivative)}$$",
                f"Simplified result: $${sp.latex(simplified)}$$"
            ]

            final_answer = sp.latex(simplified)

        # ─────────────────────────────────────────────
        # STANDARD DIFFERENTIATION (KEYWORD BASED)
        # ─────────────────────────────────────────────
        elif any(k in text for k in ["differentiate", "derivative of", "find the derivative"]):
            expr_text = re.sub(
                r"find the derivative of|differentiate|derivative of",
                "",
                text
            ).strip()

            expr = sp.sympify(expr_text)
            vars_ = sorted(expr.free_symbols, key=lambda s: s.name)
            var = vars_[0] if vars_ else sp.symbols("x")

            derivative = sp.diff(expr, var)
            simplified = sp.simplify(derivative)

            steps = [
                f"Expression: $${sp.latex(expr)}$$",
                f"Differentiate with respect to $${sp.latex(var)}$$",
                f"Derivative: $${sp.latex(derivative)}$$",
                f"Simplified result: $${sp.latex(simplified)}$$"
            ]

            final_answer = sp.latex(simplified)

        # ─────────────────────────────────────────────
        # GRADIENT
        # ─────────────────────────────────────────────
        elif "gradient" in text:
            expr_text = re.sub(r"gradient of", "", text).strip()
            expr = sp.sympify(expr_text)

            vars_ = sorted(expr.free_symbols, key=lambda s: s.name)
            grad = [sp.diff(expr, v) for v in vars_]

            steps = [
                f"Function: $${sp.latex(expr)}$$",
                f"Variables: $${', '.join(map(sp.latex, vars_))}$$",
                f"Gradient: $${sp.latex(sp.Matrix(grad))}$$"
            ]

            final_answer = sp.latex(sp.Matrix(grad))

        # ─────────────────────────────────────────────
        # JACOBIAN
        # ─────────────────────────────────────────────
        elif "jacobian" in text:
            funcs = re.findall(r"\[(.*?)\]", text)[0]
            funcs = [sp.sympify(f) for f in funcs.split(",")]

            vars_ = sorted(
                set().union(*[f.free_symbols for f in funcs]),
                key=lambda s: s.name
            )

            J = sp.Matrix(funcs).jacobian(vars_)

            steps = [
                f"Functions: $${sp.latex(sp.Matrix(funcs))}$$",
                f"Variables: $${', '.join(map(sp.latex, vars_))}$$",
                f"Jacobian Matrix: $${sp.latex(J)}$$"
            ]

            final_answer = sp.latex(J)

        # ─────────────────────────────────────────────
        # HESSIAN
        # ─────────────────────────────────────────────
        elif "hessian" in text:
            expr_text = re.sub(r"hessian of", "", text).strip()
            expr = sp.sympify(expr_text)

            vars_ = sorted(expr.free_symbols, key=lambda s: s.name)
            H = sp.hessian(expr, vars_)

            steps = [
                f"Function: $${sp.latex(expr)}$$",
                f"Variables: $${', '.join(map(sp.latex, vars_))}$$",
                f"Hessian Matrix: $${sp.latex(H)}$$"
            ]

            final_answer = sp.latex(H)

        # ─────────────────────────────────────────────
        # INDEFINITE INTEGRAL
        # ─────────────────────────────────────────────
        elif "integrate" in text and "from" not in text:
            expr_text = re.sub(r"integrate", "", text).strip()
            expr = sp.sympify(expr_text)

            var = sorted(expr.free_symbols, key=lambda s: s.name)[0]
            integral = sp.integrate(expr, var)

            steps = [
                f"Integrand: $${sp.latex(expr)}$$",
                f"Variable: $${sp.latex(var)}$$",
                f"Indefinite Integral: $${sp.latex(integral)} + C$$"
            ]

            final_answer = sp.latex(integral) + " + C"

        # ─────────────────────────────────────────────
        # DEFINITE INTEGRAL
        # ─────────────────────────────────────────────
        elif "from" in text:
            match = re.search(r"from (.*?) to (.*?)$", text)
            bounds = match.groups()

            expr_text = re.sub(r"integrate|from .*", "", text).strip()
            expr = sp.sympify(expr_text)

            var = sorted(expr.free_symbols, key=lambda s: s.name)[0]
            result = sp.integrate(expr, (var, bounds[0], bounds[1]))

            steps = [
                f"Integrand: $${sp.latex(expr)}$$",
                f"Bounds: $${bounds[0]}$ to $${bounds[1]}$$",
                f"Definite Integral Result: $${sp.latex(result)}$$"
            ]

            final_answer = sp.latex(result)

        # ─────────────────────────────────────────────
        # LIMIT
        # ─────────────────────────────────────────────
        elif "limit" in text:
            expr_text = re.sub(r"limit", "", text).strip()
            expr = sp.sympify(expr_text)

            var = sorted(expr.free_symbols, key=lambda s: s.name)[0]
            result = sp.limit(expr, var, 0)

            steps = [
                f"Expression: $${sp.latex(expr)}$$",
                f"Taking limit as $${sp.latex(var)} \\to 0$$",
                f"Limit result: $${sp.latex(result)}$$"
            ]

            final_answer = sp.latex(result)

        # ─────────────────────────────────────────────
        # TAYLOR SERIES
        # ─────────────────────────────────────────────
        elif "taylor" in text:
            expr_text = re.sub(r"taylor series of", "", text).strip()
            expr = sp.sympify(expr_text)

            var = sorted(expr.free_symbols, key=lambda s: s.name)[0]
            series = sp.series(expr, var, 0, 5)

            steps = [
                f"Function: $${sp.latex(expr)}$$",
                f"Taylor expansion around $${sp.latex(var)} = 0$$",
                f"Series: $${sp.latex(series)}$$"
            ]

            final_answer = sp.latex(series)

        else:
            final_answer = "Problem type not recognized."
            steps = ["Unable to match problem to a supported operation."]

    except Exception as e:
        final_answer = "Symbolic computation failed."
        steps = [f"Error: {str(e)}"]

    retrieved_context = retrieve_context(problem_text, top_k=3) or []

    return {
        "final_answer": final_answer,
        "steps": steps,
        "used_context": list(
            {ctx.get("source") for ctx in retrieved_context if isinstance(ctx, dict)}
        ),
        "used_memory": False
    }
