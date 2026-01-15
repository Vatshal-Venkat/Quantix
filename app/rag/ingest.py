from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import re

BASE_DIR = Path(__file__).resolve().parents[1]
KB_PATH = BASE_DIR / "knowledge_base"
VECTORSTORE_PATH = BASE_DIR / "data" / "vectorstore"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def chunk_markdown_qa(text: str):
    """
    Chunk strictly by Q/A blocks:
    ### Q<number>.
    ...
    **Answer:** ...
    """
    pattern = r"(### Q\d+\.[\s\S]*?\*\*Answer:\*\*[^\n]*)"
    return re.findall(pattern, text)


def ingest():
    VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)

    model = SentenceTransformer(MODEL_NAME)

    texts, metadatas = [], []

    for file in KB_PATH.glob("*.md"):
        content = file.read_text(encoding="utf-8")
        chunks = chunk_markdown_qa(content)

        for chunk in chunks:
            texts.append(chunk.strip())
            metadatas.append({
                "source": file.name,
                "type": "jee_pyq"
            })

    if not texts:
        raise RuntimeError("No QA chunks found. Check markdown format.")

    embeddings = model.encode(texts, convert_to_numpy=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, str(VECTORSTORE_PATH / "index.faiss"))

    with open(VECTORSTORE_PATH / "meta.pkl", "wb") as f:
        pickle.dump({"texts": texts, "metadatas": metadatas}, f)

    print(f"✅ Ingested {len(texts)} QA chunks")


if __name__ == "__main__":
    ingest()
