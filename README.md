

---

```markdown
# 🧠 RAG Math Assistant

This project is a **Retrieval-Augmented Generation (RAG)**-powered math assistant with three main components:

1. **Data Ingestion** — One-time script to populate your vector database.  
2. **Backend Server (FastAPI)** — The "brain" of the system.  
3. **Frontend App (React)** — The user-facing chat interface.

---

## 🚀 Project Structure

```

project/
├── backend/              # FastAPI backend
│   ├── app/              # API source code
│   ├── requirements.txt  # Python dependencies
│   └── .env.example      # Example environment variables
├── frontend/             # React frontend
│   ├── src/              # React source code
│   └── package.json      # Node dependencies
└── scripts/
└── ingest_math_dataset.py  # One-time ingestion script

````

---

## 🧩 Prerequisites

Before you begin, make sure you have:

- **Python 3.9+**
- **Node.js 16+**
- **npm**
- **Qdrant instance running** (local or cloud)
- **API keys** for:
  - Google
  - Qdrant
  - Tavily

---

## ⚙️ Part 1: Backend Setup

The backend is the **core** of your RAG system — it handles retrieval, reasoning, and model orchestration.

### 1️⃣ Navigate to the Backend Folder
```bash
cd /path/to/your/project/backend/
````

### 2️⃣ Create and Activate a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

* **macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```
* **Windows:**

  ```bash
  .\venv\Scripts\activate
  ```

*(You’ll know it’s active when you see `(venv)` at the start of your terminal prompt.)*

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

* Find the file `.env.example`
* Rename it to `.env`
* Open `.env` and fill in your actual API keys for **Google**, **Qdrant**, and **Tavily**

### 5️⃣ One-Time Data Ingestion

This step populates your Qdrant vector database with math dataset embeddings.

```bash
python ../scripts/ingest_math_dataset.py
```

You should see:

```
Ingestion complete.
```

### 6️⃣ Run the Backend Server

```bash
uvicorn app.main:app --reload
```

If successful, your terminal will show something like:

```
--- LangChain Gemini Client Initialized ---
--- Qdrant Client Initialized ---
--- SentenceTransformer Model Loaded ---
--- Tavily Client Initialized (Simulating MCP) ---
--- DSPy Client Initialized and Configured ---
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Leave this terminal running!
This will be **Terminal 1**.

---

## 💻 Part 2: Frontend Setup

The frontend is your **React-based chat interface** that connects to the backend.

### 1️⃣ Open a New Terminal

Keep the backend running in Terminal 1.
Open **Terminal 2** for the frontend.

### 2️⃣ Navigate to the Frontend Folder

```bash
cd /path/to/your/project/frontend/
```

### 3️⃣ Install Node Dependencies

```bash
npm install
```

### 4️⃣ Start the Frontend App

```bash
npm start
```

Your browser should automatically open at:

```
http://localhost:3000
```

If successful, your terminal will show:

```
Compiled successfully!
```

---

## 🧪 Part 3: Test the Full Application

✅ **Terminal 1:** Backend logs showing server activity
✅ **Terminal 2:** Frontend showing "Compiled successfully"
✅ **Browser:** App running at [http://localhost:3000](http://localhost:3000)

Now you can chat with your math assistant and test RAG-powered responses!

---

## 🛠️ Troubleshooting

| Issue                   | Possible Fix                                                |
| ----------------------- | ----------------------------------------------------------- |
| `ModuleNotFoundError`   | Recheck your virtual environment and reinstall dependencies |
| Backend not starting    | Ensure `.env` is properly configured                        |
| Frontend not connecting | Check backend URL in frontend config                        |
| Qdrant connection error | Make sure Qdrant is running and accessible                  |

---

## 🧾 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Your Name**
Built with ❤️ using FastAPI, React, LangChain, and Qdrant.

```

---

Would you like me to include a **section for deployment (Docker or cloud hosting)** in the README as well? It’s often helpful for production use.
```
