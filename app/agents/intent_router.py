def route_intent(parsed_problem: dict) -> str:
    topic = parsed_problem.get("topic")

    if topic == "calculus":
        return "calculus_derivative"
    elif topic == "probability":
        return "probability_basic"
    elif topic == "linear_algebra":
        return "linear_algebra_basic"
    elif topic == "algebra":
        return "algebra_basic"
    else:
        return "fallback_llm"
