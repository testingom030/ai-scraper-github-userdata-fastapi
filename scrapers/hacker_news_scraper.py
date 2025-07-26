# scrapers/hacker_news_scraper.py
import os
import httpx
from bs4 import BeautifulSoup
import google.generativeai as genai
from pydantic import BaseModel, HttpUrl, ValidationError

# Configure the Gemini API client
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class HackerNewsStory(BaseModel):
    """Pydantic model to validate scraped story data."""
    rank: int
    title: str
    link: HttpUrl

async def scrape_top_stories() -> list[HackerNewsStory]:
    """Scrapes the top stories from the Hacker News homepage."""
    url = "https://news.ycombinator.com/"
    stories = []
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0, follow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.find_all("tr", class_="athing")

            for item in items:
                rank_tag = item.find("span", class_="rank")
                title_tag = item.find("span", class_="titleline").find("a")
                
                if rank_tag and title_tag:
                    try:
                        story_data = {
                            "rank": int(rank_tag.text.strip(".")),
                            "title": title_tag.text,
                            "link": title_tag["href"]
                        }
                        # Validate data with Pydantic model
                        stories.append(HackerNewsStory(**story_data))
                    except (ValueError, ValidationError) as e:
                        print(f"Skipping a story due to parsing/validation error: {e}")
            
            return stories

        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url}.")
            return []

async def summarize_headlines_with_gemini(stories: list[HackerNewsStory]) -> str:
    """Uses Google's Gemini Flash model to summarize a list of headlines."""
    if not stories:
        return "No headlines provided to summarize."

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Create a single string of headlines
    headlines_text = "\n".join([f"{story.rank}. {story.title}" for story in stories])
    
    prompt = f"""
    You are a witty tech analyst. Based on the following top headlines from Hacker News, provide a short, insightful, and slightly humorous summary of the current state of the tech world. What are the key trends?

    Headlines:
    {headlines_text}
    
    Your Summary:
    """
    
    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return "Failed to generate summary due to an API error."