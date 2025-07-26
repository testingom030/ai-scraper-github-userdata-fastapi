# scrapers/github_scraper.py
import httpx
from typing import Dict, Union, List

async def scrape_github(username: str) -> Dict[str, Union[str, List[Dict]]]:
    try:
        async with httpx.AsyncClient() as client:
            user_url = f"https://api.github.com/users/{username}"
            repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"

            user_response = await client.get(user_url)
            user_data = user_response.json()

            if "message" in user_data:
                return {"error": user_data["message"]}

            repos_response = await client.get(repos_url)
            repos_data = repos_response.json()

            if isinstance(repos_data, dict) and "message" in repos_data:
                return {"error": repos_data["message"]}

            if not isinstance(repos_data, list):
                return {"error": "Invalid response from GitHub API"}

            extracted_repos = []
            for repo in repos_data:
                extracted_repos.append({
                    "name": repo.get("name"),
                    "html_url": repo.get("html_url"),
                    "description": repo.get("description"),
                    "language": repo.get("language"),
                    "stargazers_count": repo.get("stargazers_count"),
                    "forks_count": repo.get("forks_count"),
                    "created_at": repo.get("created_at"),
                    "updated_at": repo.get("updated_at")
                })

            return {
                "user": {
                    "login": user_data.get("login"),
                    "name": user_data.get("name"),
                    "bio": user_data.get("bio"),
                    "location": user_data.get("location"),
                    "public_repos": user_data.get("public_repos"),
                    "followers": user_data.get("followers"),
                    "following": user_data.get("following"),
                    "created_at": user_data.get("created_at")
                },
                "repositories": sorted(extracted_repos, key=lambda x: x["stargazers_count"], reverse=True)
            }

    except Exception as e:
        return {"error": f"Failed to fetch GitHub data: {str(e)}"}
