Here’s a clean, professional **README.md** file version of your project description, formatted for GitHub (with Markdown best practices, proper structure, and emoji headers).

---

```markdown
# 🧮 Human-in-the-Loop: The Math Routing Agent

**An intelligent "Math Professor" built with Agentic RAG + Human Feedback.**  
This full-stack AI application uses a modern Agentic-RAG pipeline to answer mathematical questions, fallback to web search for unknown queries, and improve continuously using DSPy-powered Human-in-the-Loop (HITL) learning.

---


---

## ✨ Core Features

### 1. 🧠 Intelligent RAG Routing
- The agent first checks a **Qdrant Cloud VectorDB** for a similar math problem.  
- If a **high-confidence match** is found, it uses that context to answer (source: `knowledge_base`).

### 2. 🌐 MCP Web Search Fallback
- If the question isn’t in the knowledge base (e.g., arithmetic, new word problem),  
  the agent automatically performs a **web search using Tavily** (source: `web_search`).

### 3. 🧩 AI Gateway (Guardrails)
- **Input Guardrail:** An LLM-based filter that rejects non-math or off-topic questions.  
- **Output Guardrail:** A Python-based check that ensures the AI never replies with a refusal like “I can’t answer that.”

### 4. 🔁 DSPy-Powered Human-in-the-Loop (HITL)
- Users can rate each answer: **👍 Good** or **👎 Bad**.  
- All feedback is logged to `feedback_log.jsonl`.  
- If feedback is “Bad,” the backend uses a **DSPy RefinementModule** to re-generate a better answer (source: `refined`).

### 5. 🧬 Automated Self-Learning
- The `/run-optimization` endpoint uses **DSPy’s BootstrapFewShot optimizer** to read feedback logs and fine-tune prompts.  
- Optimized parameters are saved to `optimized_refiner_module.json` and reloaded on server restart — completing the self-learning loop.

---

## 🏗️ Architecture Overview

This project uses a **modular, stateless API architecture** with clean separation of concerns.

### 🔹 Frontend (Vercel)
- Built with **React.js**
- “Dumb” client that sends and receives JSON via the API

### 🔹 Backend (Hugging Face Spaces)
- **FastAPI** server with two main endpoints:
  - `POST /ask` → Runs full RAG + Web Search pipeline  
  - `POST /feedback` → Logs feedback and optionally runs DSPy refinement

### 🔹 External Services
| Component | Service | Purpose |
|------------|----------|----------|
| Vector DB | **Qdrant Cloud** | RAG Knowledge Base |
| Web Search | **Tavily (MCP)** | Fallback search for unknown math questions |
| LLM | **Google Gemini** | Core reasoning, guardrails, and refinement |
| Embeddings | **sentence-transformers** | Vectorizing queries & documents |
| HITL | **DSPy** | Feedback-driven refinement and optimization |

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|-----------|-------------|----------|
| Backend | FastAPI, Uvicorn | High-performance API server |
| Frontend | React.js | Modern, responsive UI |
| AI Orchestration | DSPy | HITL refinement & optimization |
| Vector DB | Qdrant Cloud | RAG data storage |
| Web Search | Tavily | External search fallback |
| Embeddings | sentence-transformers | Semantic search |
| Deployment | Hugging Face Spaces, Vercel | Hosting backend & frontend |

---

## 🧰 Prerequisites

Ensure you have the following installed:
- Python **3.11+**
- Node.js **18+**
- Git

Create a `.env` file (see `.env.example`) with:
```

GOOGLE_API_KEY=
QDRANT_API_KEY=
VECTORDB_URL=
TAVILY_API_KEY=

````

---

## 🧩 Setup Instructions

### Step 1: Ingest Data (One-Time Setup)
Populate your **Qdrant database** before running the app.

```bash
# Clone the repository
git clone https://github.com/abhikamui/Math-Rag-Agent.git
cd YOUR_REPO

# Install backend dependencies
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the ingestion script (reads .env automatically)
python ../scripts/ingest_math_dataset.py
````

---

### Step 2: Run the Backend

```bash
# Inside the /backend folder (with venv active)
uvicorn app.main:app --reload
```

Your backend should now be running on **[http://localhost:8000](http://localhost:8000)**

---

### Step 3: Run the Frontend

```bash
# Open a new terminal
cd ../frontend

# Install dependencies
npm install

# Start the React app
npm start
```

The frontend will open automatically at **[http://localhost:3000](http://localhost:3000)**

---

## 🚀 Deployment

### Backend (Hugging Face Spaces)

* Uses `backend/Dockerfile` for container build
* Deploy on **CPU Basic Space (16GB RAM)** for embeddings & models
* Add API keys as **Secrets** in Hugging Face Space settings
* `HF_HOME` and `DISKCACHE_DIR` set in Dockerfile to prevent permission issues

### Frontend (Vercel)

* Deploy `/frontend` as a static site
* Set environment variables:

  * `REACT_APP_API_URL` → Your Hugging Face backend URL
  * `FRONTEND_URL` → Your Vercel frontend URL (for CORS)

---

## 🧑‍🏫 Example Flow

1. User asks a math question →
   Agent searches **Qdrant** for similar context
2. If no match → performs **web search via Tavily**
3. Generates answer via **Gemini**
4. User rates response → stored in `feedback_log.jsonl`
5. Poor ratings trigger **DSPy refinement**
6. Optimizer learns from feedback → improves prompts automatically

---

## 🧩 Folder Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── pipelines/
│   │   ├── routes/
│   │   └── utils/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── scripts/
│   └── ingest_math_dataset.py
│
├── feedback_log.jsonl
├── optimized_refiner_module.json
└── README.md
```

---

## 🧠 Future Improvements

* Add **step-by-step math reasoning visualization**
* Implement **multi-turn conversation memory**
* Extend support for **physics and statistics problems**
* Add **auto-refresh dashboard** for feedback analysis

---

## 📜 License

This project is released under the **MIT License** — free for personal and educational use.

---

## 👨‍💻 Author

Built with ❤️ by **[Kamuni Abhilash]**
📧 Contact: abhilashkamuni60@gmail.com
🌐 GitHub: https://github.com/abhikamuni

---
