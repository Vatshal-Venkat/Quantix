# 🧠 Multimodal Math Mentor

An AI-powered symbolic mathematics system capable of **understanding, solving, and explaining mathematical problems** across calculus, linear algebra, and multivariable analysis using **symbolic reasoning**, **retrieval-augmented knowledge**, and a **clean interactive UI**.

---

## 🚀 Overview

**Multimodal Math Mentor** accepts math problems in **text, image, or audio form**, parses the intent, performs **exact symbolic computation**, and returns:

- ✅ A **correct mathematical result**
- 🧩 **Step-by-step symbolic reasoning**
- 📐 **LaTeX-rendered equations**
- 📚 Supporting sources via RAG
- 🧠 Optional memory reuse from past verified solutions

The system is built with **FastAPI + vanilla HTML/CSS/JS**, ensuring low latency, full control, and zero frontend bloat.

---

## ✨ Features

### Core Capabilities
- Symbolic differentiation (single & multi-variable)
- Gradients, Jacobians, and Hessians
- Indefinite & definite integrals
- Limits & Taylor series expansion
- Algebraic equation solving
- Step-by-step symbolic explanations

### AI & Systems Features
- Retrieval-Augmented Generation (RAG) for contextual grounding
- Memory-based solution reuse via feedback loop
- Robust parsing and defensive execution
- Clean JSON-based agent contracts

### UI / UX
- Modern, card-based layout
- MathJax-powered LaTeX rendering
- Fast, minimal, framework-free frontend
- Professional, futuristic, and readable design

---

## 🧱 Architecture

Frontend (HTML/CSS/JS)
│
▼
FastAPI Backend
│
├── Parser Agent
├── Intent Router
├── Solver Agent (SymPy)
├── Verifier Agent
├── Explainer Agent
├── RAG Retriever (FAISS)
└── Memory Store


---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Python
- **Symbolic Math:** SymPy
- **Vector Search:** FAISS
- **Frontend:** HTML, CSS, JavaScript
- **Math Rendering:** MathJax
- **AI Patterns:** RAG, agent-based design

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/multimodal-math-mentor.git
cd multimodal-math-mentor
```
---

### 2 Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

---
### 3 Install dependencies
```bash
Install Dependencies
```
