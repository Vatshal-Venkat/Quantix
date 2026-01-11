import numpy as np
from sentence_transformers import SentenceTransformer
from app.memory.memory_store import load_memory

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def find_similar_problem(query_text: str, threshold: float = 0.85):
    memory = load_memory()
    if not memory:
        return None

    query_embedding = model.encode(query_text)

    best_match = None
    best_score = 0.0

    for item in memory:
        score = cosine_similarity(query_embedding, item["embedding"])
        if score > best_score and score >= threshold:
            best_score = score
            best_match = item

    return best_match
