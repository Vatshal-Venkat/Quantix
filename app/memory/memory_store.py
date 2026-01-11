import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

MEMORY_PATH = Path("data/memory.json")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def load_memory():
    if not MEMORY_PATH.exists():
        return []
    return json.loads(MEMORY_PATH.read_text())


def store_interaction(problem, solution, feedback, correction=None):
    MEMORY_PATH.parent.mkdir(exist_ok=True)

    memory = load_memory()

    embedding = model.encode(problem["problem_text"]).tolist()

    memory.append({
        "embedding": embedding,
        "topic": problem.get("topic"),
        "problem_text": problem.get("problem_text"),
        "solution_steps": solution.get("steps"),
        "final_answer": solution.get("final_answer"),
        "feedback": feedback,
        "correction": correction
    })

    MEMORY_PATH.write_text(json.dumps(memory, indent=2))
