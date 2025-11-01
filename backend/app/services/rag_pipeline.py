from app.core.clients import (
    qdrant_client, 
    embedding_model, 
    tavily_client, 
    llm_gemini
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- RAG Prompt Template ---
MATH_PROFESSOR_PROMPT = """
You are a helpful Math Professor. Your goal is to teach a student by providing a clear,
step-by-step solution to their question.

You will be given a user's question and some context (if any was found).
- The context is from: {source}
- If the context is from the 'knowledge_base', it's a similar problem. Use it as a reference.
- If the context is from the 'web', it's background information. Synthesize it.
- If there is no context, solve the problem directly.

**TASK:**
1.  Acknowledge the user's question.
2.  Provide a **simplified, step-by-step solution** as if explaining it to a student.
3.  Break down complex terms.
4.  End with the final, clear answer.

**Context:**
{context}

**User Question:**
{question}

**Your Step-by-Step Solution:**
"""

def search_knowledge_base(question: str) -> str | None:
    """
    Searches the Qdrant VectorDB for a relevant math problem.
    """
    if not qdrant_client:
        print("--- RAG: Qdrant client not available. Skipping KB search. ---")
        return None
        
    print("--- RAG: Searching Knowledge Base ---")
    try:
        vector = embedding_model.encode(question).tolist()
        
        search_result = qdrant_client.search(
            collection_name="math_problems", # Must match ingest script
            query_vector=vector,
            limit=1,
            score_threshold=0.60 # Flexible threshold
        )
        
        if not search_result:
            print("--- RAG: No KB result found (Score < 0.60). ---")
            return None
        
        top_score = search_result[0].score
        payload = search_result[0].payload
        context = (
            f"Found a similar problem (score: {top_score:.2f}):\n"
            f"Question: {payload['question']}\n"
            f"Solution: {payload['answer']}\n"
            f"Steps: {payload['steps']}"
        )
        print(f"--- RAG: Found KB context. Score: {top_score} ---")
        return context

    except Exception as e:
        print(f"--- RAG: Error in KB search: {e} ---")
        return None

def search_web_mcp(question: str) -> str | None:
    """
    Performs a web search using Tavily.
    This simulates your MCP pipeline's functionality.
    """
    print("--- RAG: No KB hit. Searching Web (Simulating MCP)... ---")
    try:
        response = tavily_client.search(
            query=f"step-by-step solution for math problem: {question}",
            search_depth="advanced",
            max_results=3
        )
        
        # Format the results into a single context string
        context = "Found web context:\n\n"
        for result in response.get("results", []):
            context += f"URL: {result['url']}\nContent: {result['content']}\n\n"
        
        print("--- RAG: Found Web context. ---")
        return context
    
    except Exception as e:
        print(f"--- RAG: Error in Web/MCP search: {e} ---")
        return None

async def generate_solution(question: str) -> (str, str):
    """
    The main RAG pipeline function.
    Returns: (solution, source)
    """
    context = None
    source = "none"

    # 1. Try Knowledge Base (RAG)
    context_kb = search_knowledge_base(question)
    
    if context_kb:
        context = context_kb
        source = "knowledge_base"
    else:
        # 2. Fallback to Web Search (MCP)
        context_web = search_web_mcp(question)
        if context_web:
            context = context_web
            source = "web_search"
    
    if not context:
        context = "No additional context found. Solve the problem directly."
        source = "direct_answer"

    # 3. Generate the solution
    print(f"--- RAG: Generating solution with source: {source} ---")
    prompt = ChatPromptTemplate.from_template(MATH_PROFESSOR_PROMPT)
    chain = prompt | llm_gemini | StrOutputParser()
    
    try:
        solution = await chain.ainvoke({
            "source": source,
            "context": context,
            "question": question
        })
        return solution, source
    except Exception as e:
        print(f"--- RAG: Error in final LLM generation: {e} ---")
        return f"Sorry, I encountered an error while generating the solution: {e}", "error"

