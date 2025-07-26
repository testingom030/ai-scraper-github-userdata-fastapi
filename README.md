
# AI-Powered Social Media Scraper API

This project is a powerful API built with FastAPI that scrapes public data from social media platforms like GitHub and LinkedIn, analyzes the data using Google's Gemini AI model, and returns a structured JSON analysis. It uses advanced techniques like browser automation with Playwright to handle modern, JavaScript-heavy websites and Redis for efficient caching of results.

## 🚀 Live Demo

The API is deployed and live on Render. You can interact with it directly.

-   **Base URL**: `https://ai-scraper-github-userdata-fastapi.onrender.com`
-   **Interactive Docs**: [`https://ai-scraper-github-userdata-fastapi.onrender.com/docs`](https://ai-scraper-github-userdata-fastapi.onrender.com/docs)
-   **Status**: ![API is online](https://img.shields.io/badge/API-online-green)

## ✨ Features

-   **Multi-Platform Scraping**: Currently supports scraping public profiles from:
    -   GitHub (Usernames)
    -   LinkedIn (Public Profile URLs)
-   **AI-Powered Analysis**: Leverages the `gemini-1.5-flash` model to provide intelligent, structured summaries of scraped data.
-   **Robust Scraping Engine**: Uses Playwright to simulate a real browser, allowing it to bypass basic bot detection and handle dynamic content.
-   **Efficient Caching**: Integrated with Redis to cache results, providing near-instant responses for repeated requests and reducing API costs.
-   **Containerized & Deployable**: Fully containerized with Docker and Docker Compose for easy local setup and scalable deployment.

## 🛠️ Tech Stack

-   **Backend**: FastAPI, Python 3.9
-   **Scraping**: Playwright
-   **AI Model**: Google Gemini
-   **Database/Cache**: Redis
-   **Containerization**: Docker & Docker Compose
-   **Hosting**: Render

## 📖 API Usage

You can interact with the live API through the [interactive documentation](https://ai-scraper-github-userdata-fastapi.onrender.com/docs) or by using a tool like `curl` or Postman.

### Scrape a Profile

-   **Endpoint**: `POST /scrape`
-   **Description**: Scrapes a target from a specified platform and returns an AI-powered analysis.
-   **Request Body**:
    ```json
    {
      "platform": "string",
      "target": "string"
    }
    ```

#### `curl` Examples (Live API):

**Scraping a GitHub Profile:**
```bash
curl -X 'POST' \
  '[https://ai-scraper-github-userdata-fastapi.onrender.com/scrape](https://ai-scraper-github-userdata-fastapi.onrender.com/scrape)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "platform": "github",
  "target": "torvalds"
}'
````

**Scraping a LinkedIn Profile:**

```bash
curl -X 'POST' \
  '[https://ai-scraper-github-userdata-fastapi.onrender.com/scrape](https://ai-scraper-github-userdata-fastapi.onrender.com/scrape)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "platform": "linkedin",
  "target": "[https://www.linkedin.com/in/williamhgates/](https://www.linkedin.com/in/williamhgates/)"
}'
```

## ⚙️ Local Development

To run the project on your local machine, follow these steps.

### Prerequisites

  - **Docker and Docker Compose**: [Install Docker](https://www.docker.com/products/docker-desktop/)
  - **API Keys**: You will need a Google Gemini API key.

### Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create the environment file:**
    Create a file named `.env` in the root of the project and add your key:

    ```
    # .env
    GEMINI_API_KEY="your_google_ai_api_key_goes_here"
    ```

3.  **Build and Run with Docker Compose:**

    ```bash
    docker-compose up --build
    ```

    The API will be available at `http://localhost:5000`.

## ⚠️ Disclaimer

This project is intended for educational purposes to demonstrate advanced web scraping, API development, and AI integration. Scraping websites, especially LinkedIn, can be against their Terms of Service. Users of this project are responsible for ensuring they use it ethically and in compliance with the respective platform's policies. The developers assume no liability for misuse.

```
