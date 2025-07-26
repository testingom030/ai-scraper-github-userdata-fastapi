import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from redis import asyncio as aioredis

# --- Import your scrapers ---
# Make sure these files exist and have the async functions
from scrapers.github_scraper import scrape_github
from scrapers.linkedin_scraper import scrape_linkedin

# --- Initial Setup ---
load_dotenv()

app = FastAPI(
    title="AI-Powered Social Media Scraper",
    description="An API that scrapes social media profiles and analyzes them with Google Gemini.",
    version="2.0.0"
)

# --- Redis Cache Connection ---
# Establishes a connection to Redis on startup for caching results.


# main.py

import os
# ... other imports

@app.on_event("startup")
async def startup_event():
    """Initialize Redis connection."""
    # Use the REDIS_URL from Render's environment, or fall back to the Docker Compose name for local dev
    redis_url = os.getenv("REDIS_URL", "redis://redis")
    try:
        app.state.redis = await aioredis.from_url(redis_url, decode_responses=True)
        print(f"Successfully connected to Redis at {redis_url}.")
    except Exception as e:
        print(f"Could not connect to Redis: {e}. Caching will be disabled.")
        app.state.redis = None


@app.on_event("shutdown")
async def shutdown_event():
    """Close Redis connection."""
    if app.state.redis:
        await app.state.redis.close()
        print("Redis connection closed.")

# --- Pydantic Models ---
class ScrapeRequest(BaseModel):
    platform: str
    target: str  # e.g., a username or a full URL

# --- Gemini Configuration and Processing ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not found.")
genai.configure(api_key=GEMINI_API_KEY)

async def process_with_gemini(data: dict, platform: str) -> dict:
    """
    Analyzes scraped data using the Gemini 1.5 Flash model with JSON mode.
    """
    # This configuration tells Gemini to ONLY output a valid JSON object.
    generation_config = genai.types.GenerationConfig(
        response_mime_type="application/json"
    )
    model = genai.GenerativeModel(
        "gemini-1.5-flash-latest",
        generation_config=generation_config
    )

    if platform == "github":
        prompt = f"""
        Analyze the provided GitHub profile data. Your response MUST be a valid JSON object.
        Based on the repositories, languages, and descriptions, provide insights on the user's:
        1.  `primary_focus`: The main area of development (e.g., "Web Development", "Data Science").
        2.  `top_projects`: A list of 1-3 most significant projects, noting their stars and forks.
        3.  `key_skills`: A list of key programming languages and technologies observed.

        Input data: {json.dumps(data)}
        """
    else: # Generic prompt for other platforms like LinkedIn
        prompt = f"""
        Analyze the provided {platform} profile data. Your response MUST be a valid JSON object.
        Based on the data, provide insights on the user's:
        1. `professional_summary`: A brief, one-sentence summary of their professional profile.
        2. `focus_areas`: A list of their key professional skills or focus areas.
        3. `notable_highlights`: A list of 1-3 notable achievements or highlights from their profile.
        
        Input data: {json.dumps(data)}
        """
    
    try:
        # Use the async version of the call
        response = await model.generate_content_async(prompt)
        # No more manual parsing needed! The response.text is guaranteed to be a JSON string.
        analyzed_data = json.loads(response.text)
        return {"analysis": analyzed_data, "raw_data": data}

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse Gemini's JSON response.")
    except Exception as e:
        print(f"Error during Gemini processing: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred with the Gemini API: {str(e)}")


# --- API Endpoints ---
@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the AI-Powered Social Media Scraper API!",
        "docs": "/docs",
        "platforms_supported": ["github", "linkedin"]
    }

@app.post("/scrape")
async def scrape_platform(request: ScrapeRequest):
    platform = request.platform.lower()
    target = request.target
    
    # --- Cache Check ---
    if app.state.redis:
        cache_key = f"scraper:{platform}:{target}"
        cached_result = await app.state.redis.get(cache_key)
        if cached_result:
            print(f"Returning cached result for {cache_key}")
            return json.loads(cached_result)

    # --- Platform Routing ---
    if platform == "github":
        scraped_data = await scrape_github(target)
    elif platform == "linkedin":
        # WARNING: Scraping LinkedIn is against their ToS and can get your IP/account banned.
        # This is for educational purposes only.
        scraped_data = await scrape_linkedin(target)
    else:
        raise HTTPException(status_code=400, detail=f"Platform '{platform}' is not supported.")

    if "error" in scraped_data:
        raise HTTPException(status_code=500, detail=scraped_data["error"])

    # --- AI Analysis ---
    result = await process_with_gemini(scraped_data, platform)

    # --- Set Cache ---
    if app.state.redis:
        # Cache the final result for 30 minutes (1800 seconds)
        await app.state.redis.set(cache_key, json.dumps(result), ex=1800)
        print(f"Cached new result for {cache_key}")

    return result

# --- Local Development Runner ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
