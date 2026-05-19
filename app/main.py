from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
import httpx
from typing import List, Dict, Any
import json

app = FastAPI(title="Search API", description="FastAPI app with SearXNG integration")

# SearXNG API endpoint
SEARXNG_URL = "http://searxng:8080"

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Read the HTML file content
    try:
        with open("app/index.html", "r") as f:
            return Response(content=f.read(), media_type="text/html")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Index page not found")

@app.get("/search/{query}")
async def search(query: str, limit: int = 10):
    """
    Search using SearXNG and return results
    """
    try:
        async with httpx.AsyncClient() as client:
            # Call SearXNG API
            response = await client.get(
                f"{SEARXNG_URL}/search",
                params={
                    "q": query,
                    "format": "json",
                    "limit": limit
                },
                headers={"X-Forwarded-For": "127.0.0.1"}
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Search failed")
            
            results = response.json()
            return {"query": query, "results": results}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during search: {str(e)}")

@app.get("/search/simple/{query}")
async def simple_search(query: str):
    """
    Simple search returning just the titles and URLs
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SEARXNG_URL}/search",
                params={
                    "q": query,
                    "format": "json"
                },
                headers={"X-Forwarded-For": "127.0.0.1"}
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Search failed")
            
            data = response.json()
            # Extract just title and url for each result
            simple_results = [
                {
                    "title": result.get("title", ""),
                    "url": result.get("url", "")
                }
                for result in data.get("results", [])
            ]
            
            # Get top 5 results for AI synthesis
            top_results = simple_results[:5]
            
            # Prepare context for LLM
            context = ""
            for result in top_results:
                if result["title"] and result["url"]:
                    context += f"Title: {result['title']}\nURL: {result['url']}\n\n"
            
            # Call OpenAI-compatible API for synthesis
            ai_summary = ""
            if context.strip():
                try:
                    llm_response = await client.post(
                        "http://host.docker.internal:1234/v1/chat/completions",
                        json={
                            "model": "gpt-3.5-turbo",
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "You are a helpful assistant that synthesizes information from search results. Create a concise answer to the user's query based strictly on the provided search results. Do not make up information or add your own opinions."
                                },
                                {
                                    "role": "user",
                                    "content": f"Based on these search results, please provide a clear and concise summary that answers this query: {query}\n\nResults:\n{context}"
                                }
                            ],
                            "temperature": 0.5
                        },
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if llm_response.status_code == 200:
                        ai_summary = llm_response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                except Exception as e:
                    print(f"Error calling LLM: {e}")
            
            # Return results with AI summary
            return {
                "query": query, 
                "results": simple_results,
                "ai_summary": ai_summary
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during search: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
