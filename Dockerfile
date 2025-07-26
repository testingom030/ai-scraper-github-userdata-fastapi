# Use a specific, stable version of Python
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- Add these lines for Playwright ---
# Install Playwright's browser binaries and their OS dependencies
RUN playwright install --with-deps

# Copy the rest of your application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
