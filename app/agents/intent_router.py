def route_intent(parsed_problem: dict) -> str:
    operation = parsed_problem.get("operation")

    if operation == "gradient":
        return "quant_gradient"

    if operation == "derivative":
        return "quant_derivative"

    if operation == "jacobian":
        return "quant_jacobian"

    if operation == "hessian":
        return "quant_hessian"

    return "unsupported"
