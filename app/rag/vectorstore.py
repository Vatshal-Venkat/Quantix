import faiss
import pickle
from pathlib import Path

# Resolve paths relative to /app
BASE_DIR = Path(__file__).resolve().parents[1]  # points to app/
VECTORSTORE_PATH = BASE_DIR / "data" / "vectorstore"


def load_vectorstore():
    index_path = VECTORSTORE_PATH / "index.faiss"
    meta_path = VECTORSTORE_PATH / "meta.pkl"

    if not index_path.exists():
        raise FileNotFoundError(
            f"FAISS index not found at {index_path}. "
            "Run `python app/rag/ingest.py` first."
        )

    index = faiss.read_index(str(index_path))

    with open(meta_path, "rb") as f:
        meta = pickle.load(f)

    return index, meta["texts"], meta["metadatas"]
