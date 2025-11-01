import dspy
from app.core.clients import dspy_gemini_lm # Use shared DSPy client

# --- 1. Define the DSPy Signature ---
# This tells DSPy what our "program" (the LLM) should do.
class RefineSolutionSignature(dspy.Signature):
    """
    You are a Math Professor. A student was not satisfied with your
    first solution and has provided feedback.
    Your task is to generate a new, improved, and final step-by-step solution
    that directly addresses the student's feedback.
    Be humble and acknowledge the feedback.
    """
    question = dspy.InputField(desc="The original math question.")
    original_solution = dspy.InputField(desc="Your first, incorrect/insufficient solution.")
    user_feedback = dspy.InputField(desc="The student's feedback or correction.")
    
    refined_solution = dspy.OutputField(
        desc="Your new, refined step-by-step solution."
    )

# --- 2. Define the DSPy Module (Program) ---
#  ChainOfThought to make it reason better.
class RefinementModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.refiner = dspy.ChainOfThought(RefineSolutionSignature)

    def forward(self, question, original_solution, user_feedback):
        result = self.refiner(
            question=question,
            original_solution=original_solution,
            user_feedback=user_feedback
        )
        return dspy.Prediction(refined_solution=result.refined_solution)

# --- 3. Create the function our API will call ---
# initialize the module here.
dspy_refiner = RefinementModule()

try:
    dspy_refiner.load("backend/optimized_refiner_module.json")
    print("--- DSPy: Loaded optimized refinement module! ---")
except FileNotFoundError:
    print("--- DSPy: No optimized module found. Using default prompts. ---")
    

def refine_solution_with_dspy(question: str, original_solution: str, user_feedback: str) -> str:
    """
    Uses the initialized DSPy module to refine an answer.
    """
    print("--- DSPy: Refining solution with feedback ---")
    if not dspy_gemini_lm:
        print("--- DSPy: Error, LM not configured. ---")
        return "Error: DSPy is not configured."
        
    try:
        # Run the DSPy program
        prediction = dspy_refiner(
            question=question,
            original_solution=original_solution,
            user_feedback=user_feedback
        )
        print("--- DSPy: Refinement complete. ---")
        return prediction.refined_solution
    except Exception as e:
        print(f"--- DSPy: Error during refinement: {e} ---")
        return f"Sorry, I encountered an error while refining the solution: {e}"

