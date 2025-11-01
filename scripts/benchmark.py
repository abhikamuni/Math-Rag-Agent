#JEE Bench dataset convertion code
import requests
import json
from datasets import load_dataset
from tqdm import tqdm # For progress bar
import time

# Load the JEE Bench dataset
DATASET_NAME = "AI4Bharat/JEEBench"
DATASET_CONFIG = "main" 
DATASET_SPLIT = "test[:50]" 
AGENT_URL = "http://localhost:8000/ask"
RESULTS_FILE = "benchmark_results.json"

def run_benchmark():
    print(f"Loading dataset {DATASET_NAME} ({DATASET_CONFIG})...")
    try:
        dataset = load_dataset(DATASET_NAME, DATASET_CONFIG, split=DATASET_SPLIT)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        print("Please ensure 'datasets' and 'pyarrow' are installed.")
        return

    results = []
    
    print(f"Running benchmark on {len(dataset)} questions...")
    for item in tqdm(dataset):
        question = item['question']
        ground_truth = item['answer']
        
        payload = {"question": question, "student_id": "benchmark_runner"}
        
        start_time = time.time()
        try:
            response = requests.post(AGENT_URL, json=payload, timeout=45) # 45 sec timeout
            end_time = time.time()
            
            if response.status_code == 200:
                agent_response = response.json()
                results.append({
                    "question": question,
                    "ground_truth": ground_truth,
                    "agent_solution": agent_response["solution"],
                    "source": agent_response["source"],
                    "latency_seconds": end_time - start_time
                })
            else:
                results.append({
                    "question": question,
                    "ground_truth": ground_truth,
                    "agent_solution": f"Error: {response.status_code} - {response.text}",
                    "source": "error",
                    "latency_seconds": end_time - start_time
                })
        except requests.RequestException as e:
            end_time = time.time()
            results.append({
                "question": question,
                "ground_truth": ground_truth,
                "agent_solution": f"Request Error: {e}",
                "source": "error",
                "latency_seconds": end_time - start_time
            })
            
    # Save results to a file
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Benchmark complete. Results saved to '{RESULTS_FILE}'.")
    print("Next step: Run an 'LLM-as-a-judge' on the results file to score correctness.")

if __name__ == "__main__":
    run_benchmark()
