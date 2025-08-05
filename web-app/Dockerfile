# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire web-app directory
COPY . .

# Copy common module (assuming it's needed by the web app)
COPY ../common ./common

# Create a script to run either main.py or api.py
RUN echo '#!/bin/bash\n\
if [ "$1" = "streamlit" ]; then\n\
    exec streamlit run main.py --server.port 8501 --server.address 0.0.0.0\n\
elif [ "$1" = "api" ]; then\n\
    exec python api.py\n\
else\n\
    echo "Usage: $0 {streamlit|api}"\n\
    exit 1\n\
fi' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Expose ports for both applications
EXPOSE 8501 8000

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]