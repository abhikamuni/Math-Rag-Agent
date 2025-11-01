
import os
import json
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

# Import our modular services
# make sure the path is correct
from app.services.guardrails import check_input_guardrail, check_output_guardrail
from app.services.rag_pipeline import generate_solution
from app.services.dspy_feedback import refine_solution_with_dspy
from app.schemas import (
    AskRequest, AskResponse, FeedbackRequest, FeedbackResponse
)

# Initialize FastAPI
app = FastAPI(title="Math Routing Agent (Stateless HITL Version)")
CLIENT_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_URL, "https://*.hf.space"], # Allows React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.post("/ask/", response_model=AskResponse)
async def ask_math_question(request: AskRequest):
    """
    Endpoint to ask the Math Agent a question.
    This is a stateless request-response.
    """
    # 1. Input Guardrail
    is_safe, reason = check_input_guardrail(request.question)
    if not is_safe:
        raise HTTPException(status_code=400, detail=f"Input blocked: {reason}")
    
    # 2. RAG + MCP Pipeline
    try:
        solution, source = await generate_solution(request.question)
    except Exception as e:
        print(f"--- Main Error (generate_solution): {e} ---")
        raise HTTPException(status_code=500, detail="Agent failed to process.")
    
    # 3. Output Guardrail (Fast, non-LLM)
    is_safe, message = check_output_guardrail(solution)
    if not is_safe:
        raise HTTPException(status_code=500, detail=f"Output blocked: {message}")
    
    # 4. Return the final response
    return AskResponse(
        solution=message,
        source=source,
        thread_id=str(uuid.uuid4()), # New ID for this "turn"
        question=request.question
    )

@app.post("/feedback/", response_model=FeedbackResponse, status_code=200)
async def give_feedback(request: FeedbackRequest):
    """
    Endpoint to receive feedback and (if "bad") get a refinement.
    """
    print(f"--- HITL: Received Feedback for {request.thread_id} ---")
    
    # 1. Log the feedback (for DSPy offline optimization)
    try:
        feedback_entry = request.model_dump()
        feedback_entry["timestamp"] = datetime.utcnow().isoformat()
        
        # We assume the backend is running in the 'backend' folder
        with open("feedback_log.jsonl", "a") as f:
            f.write(json.dumps(feedback_entry) + "\n")
        print("--- HITL: Feedback logged. ---")
    except Exception as e:
        print(f"--- HITL: Error saving feedback log: {e} ---")

    # 2. If feedback is "bad", generate a refinement
    if request.rating == "bad" and request.feedback_text:
        print(f"--- HITL: Rating is 'bad'. Generating refinement... ---")
        try:
            # 3. Run DSPy Refinement
            refined_solution = refine_solution_with_dspy(
                question=request.question,
                original_solution=request.original_solution,
                user_feedback=request.feedback_text
            )
            
            # 4. Output Guardrail (on the new solution)
            is_safe, message = check_output_guardrail(refined_solution)
            if not is_safe:
                raise HTTPException(status_code=500, detail=f"Refined output blocked: {message}")

            # 5. Return new, refined solution
            return FeedbackResponse(
                solution=message,
                source="refined", # New source
                thread_id=request.thread_id,
                question=request.question
            )
        except Exception as e:
            print(f"--- HITL: Error during refinement: {e} ---")
            raise HTTPException(status_code=500, detail="Error processing feedback.")
    
    # If rating is "good", just log it and return a different response.
    # We must return a FeedbackResponse, so we just return the original info.
    print("--- HITL: Rating is 'good'. Logging only. ---")
    return FeedbackResponse(
        solution=request.original_solution,
        source="feedback_logged",
        thread_id=request.thread_id,
        question=request.question
    )

@app.get("/")
def read_root():
    return {"Hello": "Math Agent API is running (Stateless HITL Version)."}

