def route_intent(parsed_subproblem: dict) -> str:
    operation = parsed_subproblem.get("operation")

    if operation == "gradient":
        return "quant_gradient"

    if operation == "derivative":
        return "quant_derivative"

    if operation == "jacobian":
        return "quant_jacobian"

    if operation == "hessian":
        return "quant_hessian"

    if operation == "optimization":
        return "quant_optimization"

    if operation == "system":
        return "quant_system"

    return "unsupported"
