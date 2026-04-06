# Use official Python runtime
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Set environment variables with defaults
ENV API_BASE_URL=https://api.openai.com/v1
ENV MODEL_NAME=gpt-4
ENV HF_TOKEN=""

# Run the FastAPI server
CMD ["python", "server.py"]
