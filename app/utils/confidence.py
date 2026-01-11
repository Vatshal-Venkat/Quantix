def assess_confidence(text: str) -> str:
    if not text or len(text) < 15:
        return "low"
    return "high"
