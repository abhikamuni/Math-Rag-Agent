import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')

list_of_files = [
    # Root files
    ".env.example",  # Updated to add TAVILY_API_KEY
    ".gitignore",
    "README.md",

    # Backend - Deployment and Top Level
    "backend/Dockerfile",
    "backend/requirements.txt",  # Updated to add dspy-ai, tavily, langgraph-checkpoint-sqlite
    "backend/feedback_log.jsonl", # Will be created automatically
    "backend/checkpoints.sqlite", # Will be created automatically
    
    # Backend - Application Core
    "backend/app/__init__.py",
    "backend/app/main.py",       # NEW "lifespan" version
    "backend/app/schemas.py",    # NEW file
    
    # Backend - Core Utilities
    "backend/app/core/__init__.py",
    "backend/app/core/clients.py", # NEW file - replaces old config.py
    
    # Backend - Services (Agent Logic, Guardrails, HITL)
    "backend/app/services/__init__.py",
    "backend/app/services/guardrails.py",  # NEW file - has both guardrails
    "backend/app/services/rag_pipeline.py",# NEW file - has RAG and MCP logic
    "backend/app/services/dspy_feedback.py",# NEW file - has HITL/DSPy logic

    # Frontend - Deployment and Top Level
    "frontend/package.json",
    "frontend/public/index.html",
    
    # Frontend - Source
    "frontend/src/App.css",
    "frontend/src/App.js",
    "frontend/src/index.js",
    
    # Frontend - Components
    "frontend/src/components/ChatWindow.js", # Updated for stateless HITL
    "frontend/src/components/Message.js",    # Updated for stateless HITL
    "frontend/src/components/Feedback.js",   # Updated for stateless HITL
    
    # Frontend - Services
    "frontend/src/services/api.js",  # Updated for stateless HITL
    
    # Scripts (No Change)
    "scripts/ingest_math_dataset.py",
    "scripts/optimize.py",
    "scripts/benchmark.py",
]
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir} for file: {filename}")
    
    if(not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"File already exists: {filepath}")