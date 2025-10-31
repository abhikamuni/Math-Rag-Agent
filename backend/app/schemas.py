from pydantic import BaseModel
from typing import Literal

# --- /ask endpoint ---
class AskRequest(BaseModel):
    question: str
    student_id: str # For future use

class AskResponse(BaseModel):
    solution: str
    source: str
    thread_id: str
    question: str

# --- /feedback endpoint ---
class FeedbackRequest(BaseModel):
    question: str
    original_solution: str
    feedback_text: str
    rating: Literal["good", "bad"]
    thread_id: str

class FeedbackResponse(BaseModel):
    solution: str
    source: str
    thread_id: str
    question: str

