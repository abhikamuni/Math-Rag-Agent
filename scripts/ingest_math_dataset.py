import os
import json
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from datasets import load_dataset
import uuid
from dotenv import load_dotenv
from tqdm import tqdm # For a progress bar

# --- Config ---
COLLECTION_NAME = "math_problems"
# Use GSM8K (General School Math) dataset from Hugging Face
DATASET_NAME = "gsm8k"
DATASET_CONFIG = "main" # Use the main config
DATASET_SPLIT = "train[:1000]" # Ingest first 1000 problems

def ingest_to_vectordb():
    # Load .env file to get API keys
    load_dotenv()
    QDRANT_URL = os.environ.get("VECTORDB_URL")
    QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")

    if not QDRANT_URL or not QDRANT_API_KEY:
        print("Error: VECTORDB_URL or QDRANT_API_KEY not found in .env file.")
        print("Please create a .env file based on .env.example")
        return

    # --- Init Clients ---
    print(f"Connecting to Qdrant Cloud at {QDRANT_URL}...")
    client = QdrantClient(
        url=QDRANT_URL, 
        api_key=QDRANT_API_KEY
    )
    
    print("Loading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding_dim = model.get_sentence_embedding_dimension()
    print(f"Model loaded. Embedding dimension: {embedding_dim}")

    # --- Load Dataset ---
    print(f"Loading dataset {DATASET_NAME} (split: {DATASET_SPLIT})...")
    dataset = load_dataset(DATASET_NAME, DATASET_CONFIG, split=DATASET_SPLIT)
    
    # --- Create Collection in Qdrant ---
    try:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE),
        )
        print(f"Cloud Collection '{COLLECTION_NAME}' created.")
    except Exception as e:
        print(f"Collection creation failed (it might already exist): {e}")

    # --- Encode and Ingest Data ---
    print(f"Encoding and ingesting {len(dataset)} documents...")
    points_batch = []
    
    for item in tqdm(dataset):
        # We embed the question for searching
        vector = model.encode(item['question']).tolist()
        
        # We store the question, answer, and steps in the payload
        answer_parts = item['answer'].split("####")
        steps = answer_parts[0].strip()
        answer = answer_parts[1].strip() if len(answer_parts) > 1 else steps
        
        payload = {
            "question": item['question'],
            "answer": answer,
            "steps": steps
        }
        
        points_batch.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=payload
            )
        )
        
        # Upsert in batches of 100
        if len(points_batch) >= 100:
            client.upsert(
                collection_name=COLLECTION_NAME, 
                points=points_batch,
                wait=True
            )
            points_batch = []
    
    # Ingest any remaining points
    if points_batch:
        client.upsert(
            collection_name=COLLECTION_NAME, 
            points=points_batch,
            wait=True
        )

    print(f"Ingestion complete for {COLLECTION_NAME}.")

if __name__ == "__main__":
    ingest_to_vectordb()
