from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("app/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/search/simple/{query}")
async def simple_search(query: str):
    try:
        # 1. Ask SearXNG for the raw search results
        async with httpx.AsyncClient() as client:
            searxng_response = await client.get(
                "http://searxng:8080/search",
                params={"q": query, "format": "json"},
                headers={"X-Forwarded-For": "127.0.0.1"}
            )
            searxng_response.raise_for_status()
            data = searxng_response.json()
            
            # Extract all results to return to the frontend
            raw_results = data.get("results", [])
            results = [{"title": r.get("title"), "url": r.get("url"), "content": r.get("content", "")} for r in raw_results]
            
            # 2. Ask LM Studio to synthesize those results (using only first 5)
            ai_summary = None
            try:
                # Build the prompt with only first 5 results
                top_results = raw_results[:5]
                snippets = "\n".join([f"[{i+1}] {r.get('title')}: {r.get('content', '')}" for i, r in enumerate(top_results)])
                system_prompt = "You are a highly professional, strictly factual research assistant. Answer the user's query comprehensively using ONLY the provided search results. Do NOT add outside information, conversational filler, or analogies. You MUST format your response using strict Markdown: use **bold text** for emphasis, use bullet points for lists or multiple facts, and separate distinct ideas into paragraphs. Always cite sources inline using bracketed numbers (e.g., [1], [2])."
                
                llm_payload = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Query: {query}\n\nSearch Results:\n{snippets}"}
                    ],
                    "temperature": 0.3
                }
                
                # Ping LM Studio with a 120-second timeout so it doesn't drop the connection
                llm_response = await client.post(
                    "http://host.docker.internal:1234/v1/chat/completions",
                    json=llm_payload,
                    timeout=120.0  
                )
                llm_response.raise_for_status()
                ai_summary = llm_response.json()["choices"][0]["message"]["content"]
                
            except Exception as e:
                print(f"Error calling LLM: {e}")
            
            return {"query": query, "results": results, "ai_summary": ai_summary}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during search: {e}")
