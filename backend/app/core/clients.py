import os
import dspy
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient

# --- Load Environment Variables ---
from dotenv import load_dotenv
# This path goes up two directories (app -> backend) and finds .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
VECTORDB_URL = os.environ.get("VECTORDB_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

if not all([GOOGLE_API_KEY, VECTORDB_URL, QDRANT_API_KEY, TAVILY_API_KEY]):
    print("WARNING: One or more environment variables are missing from .env")
    print(f"GOOGLE_API_KEY: {'SET' if GOOGLE_API_KEY else 'MISSING'}")
    print(f"VECTORDB_URL: {'SET' if VECTORDB_URL else 'MISSING'}")
    print(f"QDRANT_API_KEY: {'SET' if QDRANT_API_KEY else 'MISSING'}")
    print(f"TAVILY_API_KEY: {'SET' if TAVILY_API_KEY else 'MISSING'}")

# --- 1. LangChain Client (for main generation) ---
llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.0
)
print("--- LangChain Gemini Client Initialized ---")

# --- 2. Qdrant Client & Embedding Model (for RAG) ---
try:
    qdrant_client = QdrantClient(
        url=VECTORDB_URL, 
        api_key=QDRANT_API_KEY,
        timeout=10 # Set a timeout
    )
    print("--- Qdrant Client Initialized ---")
except Exception as e:
    print(f"--- Qdrant Client FAILED to initialize: {e} ---")
    qdrant_client = None

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("--- SentenceTransformer Model Loaded ---")


# --- 3. Tavily Client (for MCP/Web Search) ---
# NOTE: Your project requires "MCP." In a real-world scenario, you would
# run a separate MCP server (e.g., `mcp-server up tavily`).
# For simplicity and to avoid running a *second* server, we are using
# the Tavily client directly, which is what the MCP server does internally.
# This provides the *functionality* of your MCP pipeline.
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
print("--- Tavily Client Initialized (Simulating MCP) ---")


# --- 4. DSPy Client (for Feedback/Refinement) ---
# We configure DSPy to use the same Gemini model
try:
    dspy_gemini_lm = dspy.LM(
        model="gemini-2.5-flash",
        api_key=GOOGLE_API_KEY,
        max_output_tokens=2000
    )
    dspy.configure(lm=dspy_gemini_lm)
    print("--- DSPy Client Initialized and Configured ---")
except ImportError:
    print("\n*** DSPy Error ***: `dspy-ai` package not found.")
    print("Please run `pip install dspy-ai` in your venv.\n")
    dspy_gemini_lm = None
except Exception as e:
    print(f"--- DSPy Client FAILED to initialize: {e} ---")
    dspy_gemini_lm = None

