import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')

list_of_files = [
    # Root files
    ".env.example",  
    ".gitignore",
    "README.md",

    # Backend 
    "backend/Dockerfile",
    "backend/requirements.txt",  
    "backend/feedback_log.jsonl", 
    "backend/checkpoints.sqlite", 
    
    "backend/app/__init__.py",
    "backend/app/main.py",       
    "backend/app/schemas.py",    
    
    
    "backend/app/core/__init__.py",
    "backend/app/core/clients.py",
    
    
    "backend/app/services/__init__.py",
    "backend/app/services/guardrails.py",  
    "backend/app/services/rag_pipeline.py",
    "backend/app/services/dspy_feedback.py",

    # Frontend 
    "frontend/package.json",
    "frontend/public/index.html",
    

    "frontend/src/App.css",
    "frontend/src/App.js",
    "frontend/src/index.js",
    
  
    "frontend/src/components/ChatWindow.js", 
    "frontend/src/components/Message.js",    
    "frontend/src/components/Feedback.js",   
    
   
    "frontend/src/services/api.js",  
    
    # Scripts 
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