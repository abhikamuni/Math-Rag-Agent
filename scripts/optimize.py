import os
import sys
import json
import dspy

# --- Setup Project Root ---
# This is a bit of a trick to let this script
# import files from your 'backend/app' folder.
# It adds the 'backend' directory to the Python path.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'backend'))
if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)
# --- End Setup ---

try:

    from backend.app.core.clients import dspy_gemini_lm 
    from backend.app.services.dspy_feedback import RefinementModule, RefineSolutionSignature
except ImportError as e:
    print(f"Error: {e}")
    print("Please make sure you are running this script from the root 'math-professor-project' folder,")
    print("or that your backend app structure is correct.")
    sys.exit(1)

# --- 1. Load the Feedback Log ---

def load_feedback_log(log_file_path="backend/feedback_log.jsonl"):
    """
    Loads the feedback log and filters for useful examples.
    We are looking for "bad" ratings where the user provided
    a "ground truth" correction.
    """
    print(f"Loading feedback from {log_file_path}...")
    trainset = []
    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                entry = json.loads(line)
                
                # We only want to train on "bad" feedback where the
                # user told us *why* it was bad.
                if entry.get("rating") == "bad" and entry.get("feedback_text"):
                    
                    example = dspy.Example(
                        question=entry["question"],
                        original_solution=entry["original_solution"],
                        user_feedback=entry["feedback_text"],
                        refined_solution=entry["feedback_text"] # The user's text is our "gold" answer
                    ).with_inputs("question", "original_solution", "user_feedback")
                    
                    trainset.append(example)
                    
    except FileNotFoundError:
        print(f"Error: Could not find '{log_file_path}'.")
        print("Please run the web app and submit some 'bad' feedback first.")
        return None
    
    if not trainset:
        print("No 'bad' feedback entries found in the log.")
        print("Please use the app and submit 'bad' feedback with a correction.")
        return None
        
    print(f"Loaded {len(trainset)} 'bad' feedback examples to use for training.")
    return trainset

# --- 2. Define the Evaluation Metric ---
# We'll use an "LLM-as-a-judge" to score the new, refined answers.

class AssessRefinement(dspy.Signature):
    """
    Assess the quality of a refined AI solution based on user feedback.
    The goal is to see if the refined solution *successfully incorporated*
    the user's feedback.
    """
    original_solution = dspy.InputField(desc="The AI's first, bad answer.")
    user_feedback = dspy.InputField(desc="The user's correction.")
    refined_solution = dspy.InputField(desc="The AI's new, refined answer.")
    
    assessment = dspy.OutputField(
        desc="A score from 1 to 5. 5 means the feedback was perfectly incorporated. 1 means it was ignored."
    )

def llm_as_judge_metric(gold, pred, trace=None):
    """
    DSPy metric function that uses an LLM to judge the refined output.
    'gold' is the dspy.Example (our training data).
    'pred' is the prediction from our module.
    """
    original = gold.original_solution
    feedback = gold.user_feedback
    refined = pred.refined_solution
    
    # simple Predict module for the judge
    judge = dspy.Predict(AssessRefinement)
    result = judge(
        original_solution=original,
        user_feedback=feedback,
        refined_solution=refined
    )
    

    score = 0
    try:
        score = int(result.assessment.split()[0]) 
    except:
        pass 
        
    if trace is None: 
        return score >= 4 
        

    trace.metric_score = score
    trace.metric_feedback = result.assessment
    return score >= 4


# --- 3. Run the Optimization ---

def main():
    if not dspy_gemini_lm:
        print("DSPy client not configured. Exiting.")
        return

    # 1. Load data
    trainset = load_feedback_log()
    if not trainset:
        return

    # 2. Set up the Optimizer
    # use BootstrapFewShot to generate new, high-quality
    # few-shot examples (demos) for our prompt.
    optimizer = dspy.BootstrapFewShot(
        metric=llm_as_judge_metric,
        max_bootstrapped_demos=2 # Start with 2 good examples
    )
    
    # 3. Define the "student" module we want to teach
    # This is the *un-optimized* module from our app
    student_module = RefinementModule()
    
    print("\nStarting optimization... This will take a few minutes...")
    print(f"Training on {len(trainset)} examples.")
    
    # 4. Run the compilation (optimization)
    # This will test different prompts to find what works best
    optimized_module = optimizer.compile(
        student=student_module,
        trainset=trainset
    )
    
    print("\n--- Optimization Complete! ---")

    # 5. Save the new, optimized module
    output_path = "backend/optimized_refiner_module.json"
    optimized_module.save(output_path)
    
    print(f"Saved optimized module to: {output_path}")
    
    print("\n--- Next Steps ---")
    print("To use this, you would now update 'backend/app/services/dspy_feedback.py' to load this file:")
    print("1. Add: `dspy_refiner.load(path='backend/optimized_refiner_module.json')`")
    print("This script has NOT changed your live code.")

if __name__ == "__main__":
    main()
