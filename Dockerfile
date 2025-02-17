FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable to avoid GPU warnings
ENV CUDA_VISIBLE_DEVICES="-1"

# Copy application code
COPY app/ .

# Create model directory
RUN mkdir -p /app/models

# Set working directory for model storage
VOLUME ["/app/models"]

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
