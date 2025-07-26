# AI-Powered Social Media Scraper API

This project is a powerful API built with FastAPI that scrapes public data from social media platforms like GitHub and LinkedIn, analyzes the data using Google's Gemini AI model, and returns a structured JSON analysis. It uses advanced techniques like browser automation with Playwright to handle modern, JavaScript-heavy websites and Redis for efficient caching of results.

## ✨ Features

  * **Multi-Platform Scraping**: Currently supports scraping public profiles from:
      * GitHub (Usernames)
      * LinkedIn (Public Profile URLs)
  * **AI-Powered Analysis**: Leverages the `gemini-1.5-flash` model to provide intelligent, structured summaries of scraped data.
  * **Robust Scraping Engine**: Uses Playwright to simulate a real browser, allowing it to bypass basic bot detection and handle dynamic content.
  * **Efficient Caching**: Integrated with Redis to cache results, providing near-instant responses for repeated requests and reducing API costs.
  * **Containerized & Deployable**: Fully containerized with Docker and Docker Compose for easy local setup and scalable deployment.
  * **Interactive API Docs**: Automatic, interactive API documentation provided by FastAPI at the `/docs` endpoint.

## 🛠️ Tech Stack

  * **Backend**: FastAPI, Python 3.9
  * **Scraping**: Playwright
  * **AI Model**: Google Gemini
  * **Database/Cache**: Redis
  * **Containerization**: Docker & Docker Compose

## 🚀 Getting Started

Follow these instructions to get the project running on your local machine for development and testing.

### Prerequisites

  * **Docker and Docker Compose**: Make sure you have Docker Desktop (or Docker Engine with the Compose plugin) installed and running. [Install Docker](https://www.docker.com/products/docker-desktop/)
  * **Python 3.9+** (for managing your local environment if needed).
  * **API Keys**: You will need an API key from Google AI Studio for the Gemini model.

### Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create the environment file:**
    Create a file named `.env` in the root of the project and add your Google Gemini API key:

    ```
    # .env
    GEMINI_API_KEY="your_google_ai_api_key_goes_here"
    ```

3.  **Build and Run with Docker Compose:**
    This is the recommended way to run the project. It starts both the FastAPI application and the Redis cache service with a single command.

    ```bash
    docker-compose up --build
    ```

    The API will now be running at `http://localhost:5000`.

## 📖 API Usage

You can interact with the API through the automatically generated documentation at `http://localhost:5000/docs` or by using a tool like `curl` or Postman.

### Scrape a Profile

  * **Endpoint**: `POST /scrape`
  * **Description**: Scrapes a target from a specified platform and returns an AI-powered analysis.
  * **Request Body**:
    ```json
    {
      "platform": "string",
      "target": "string"
    }
    ```

#### `curl` Examples:

**Scraping a GitHub Profile:**

```bash
curl -X 'POST' \
  'http://localhost:5000/scrape' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "platform": "github",
  "target": "torvalds"
}'
```

**Scraping a LinkedIn Profile:**

```bash
curl -X 'POST' \
  'http://localhost:5000/scrape' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "platform": "linkedin",
  "target": "https://www.linkedin.com/in/omchoksi/"
}'
```

## ☁️ Deployment

This project is ready to be deployed on platforms that support Docker, such as Render, AWS, or DigitalOcean. See the `DEPLOYMENT.md` guide for detailed instructions on deploying to Render.

## ⚠️ Disclaimer

This project is intended for educational purposes to demonstrate advanced web scraping, API development, and AI integration. Scraping websites, especially LinkedIn, can be against their Terms of Service. Users of this project are responsible for ensuring they use it ethically and in compliance with the respective platform's policies. The developers assume no liability for misuse.