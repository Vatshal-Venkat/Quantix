from sentence_transformers import SentenceTransformer
from app.rag.vectorstore import load_vectorstore

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

# Load FAISS index + metadata once at startup
index, texts, metadatas = load_vectorstore()


def retrieve_context(query: str, top_k: int = 3):
    query_embedding = model.encode([query], convert_to_numpy=True)

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        results.append({
            "content": texts[idx],
            "source": metadatas[idx]["source"]
        })

    return results
