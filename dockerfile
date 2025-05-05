# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]