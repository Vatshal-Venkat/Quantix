from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import pickle

BASE_DIR = Path(__file__).resolve().parents[1]  # points to /app
KB_PATH = BASE_DIR / "knowledge_base"
VECTORSTORE_PATH = BASE_DIR / "data" / "vectorstore"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def chunk_markdown(text: str, max_chars: int = 500):
    """
    Robust chunking for Markdown + math-heavy content.
    """
    lines = text.split("\n")
    chunks = []
    buffer = ""

    for line in lines:
        if len(buffer) + len(line) < max_chars:
            buffer += line + " "
        else:
            chunks.append(buffer.strip())
            buffer = line + " "

    if buffer.strip():
        chunks.append(buffer.strip())

    return chunks


def ingest():
    VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)

    model = SentenceTransformer(MODEL_NAME)

    texts = []
    metadatas = []

    for file in KB_PATH.glob("*.md"):
        content = file.read_text(encoding="utf-8")

        chunks = chunk_markdown(content)

        for chunk in chunks:
            if len(chunk.strip()) < 50:
                continue

            texts.append(chunk)
            metadatas.append({"source": file.name})

    if not texts:
        raise ValueError(
            "No valid chunks generated. Chunking failed."
        )

    embeddings = model.encode(texts, convert_to_numpy=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, str(VECTORSTORE_PATH / "index.faiss"))

    with open(VECTORSTORE_PATH / "meta.pkl", "wb") as f:
        pickle.dump(
            {"texts": texts, "metadatas": metadatas},
            f
        )

    print(f"Ingested {len(texts)} chunks into FAISS")


if __name__ == "__main__":
    ingest()
