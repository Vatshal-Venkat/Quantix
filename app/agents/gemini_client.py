import os
from google import genai


def get_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    # Fast + cheap, good for explanations & fallback math
    return client.models.get("gemini-1.5-flash")
