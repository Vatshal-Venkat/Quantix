# AI Planet Agent – AI-DOC Backend

A **FastAPI-based intelligent backend** that combines **Retrieval-Augmented Generation (RAG)**, **symbolic math solving**, **agent orchestration**, and **LLM fallback (Gemini)** to answer, solve, and reason over user queries with high reliability.

This system is designed to **prefer deterministic and explainable computation first**, and only fall back to LLMs when classical methods fail.

---

## Core Objectives

- Reduce hallucinations by prioritizing **retrieval + symbolic reasoning**
- Provide **structured, verifiable answers** instead of raw LLM output
- Build a **modular agent architecture** that is easy to extend
- Support **math, logic, and document-based reasoning**

---

## Tech Stack

### Backend
- FastAPI
- Uvicorn
- Python 3.10+

### Reasoning & Math
- SymPy
- Custom expression parser (implicit multiplication, power handling)

### RAG & Memory
- Context retriever module
- Similarity-based memory search
- Vector similarity logic (pluggable)

### LLM
- Gemini API (used only as a fallback agent)

---

## System Architecture

Client → FastAPI Routes → Agent Orchestrator  
→ RAG Context Retriever  
→ Similarity Memory Search  
→ Deterministic Solver (SymPy)  
→ Gemini Solver (Fallback)  
→ Structured Response

**Key Principle:**  
LLMs are the last resort, not the default solver.

---

## Project Structure

app/
├── main.py  
├── agents/  
│   ├── solver_agent.py  
│   ├── gemini_solver_agent.py  
├── rag/  
│   └── retriever.py  
├── memory/  
│   └── similarity.py  
├── utils/  
│   └── parsing.py  
└── schemas/  
    └── response.py  

---

## How Query Solving Works

1. Input received via API  
2. Relevant context retrieved (RAG)  
3. Similar problems searched from memory  
4. Symbolic solver attempts solution  
5. Gemini agent invoked only if needed  
6. Final structured response returned  

---

## Example Capabilities

- Algebraic equation solving
- Implicit math expression parsing
- Symbolic differentiation and simplification
- Context-aware question answering
- Controlled LLM fallback

---

## Installation

```bash
git clone <repo-url>
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Running the Server

```bash
uvicorn app.main:app --reload
```

Swagger UI available at:
http://127.0.0.1:8000/docs

---

## Environment Variables

Create a .env file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Why This Project Is Different

- Deterministic-first reasoning
- Symbolic + neural hybrid approach
- Modular agent pipeline
- Production-grade backend structure

---

## Roadmap

- Vector DB integration (FAISS / Chroma)
- Multi-agent routing
- Confidence scoring
- Streaming responses
- User-specific memory

---

## Author

Vatshal  
AI & Backend Systems  
Focus: Reasoning systems, RAG, symbolic–neural hybrids
