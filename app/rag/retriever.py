from sentence_transformers import SentenceTransformer
from app.rag.vectorstore import load_vectorstore
import re

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

# Load FAISS index
index, texts, metadatas = load_vectorstore()


def extract_answer(block: str) -> str | None:
    """
    Extracts **Answer:** section from markdown chunk
    """
    match = re.search(r"\*\*Answer:\*\*\s*(.+)", block)
    return match.group(1).strip() if match else None


def extract_explanation(block: str) -> str | None:
    """
    Extracts **Explanation:** section from markdown chunk
    """
    match = re.search(
        r"\*\*Explanation:\*\*(.+?)(?:\n\*\*Source:\*\*|\Z)",
        block,
        re.S
    )
    return match.group(1).strip() if match else None


def retrieve_context(query: str, top_k: int = 3):
    """
    Retrieves relevant KB chunks and extracts
    answer + explanation independently.
    """
    q_emb = model.encode([query], convert_to_numpy=True)
    _, indices = index.search(q_emb, top_k)

    results = []
    for idx in indices[0]:
        block = texts[idx]

        results.append({
            "raw": block,
            "answer": extract_answer(block),
            "explanation": extract_explanation(block),
            "source": metadatas[idx]["source"]
        })

    return results
