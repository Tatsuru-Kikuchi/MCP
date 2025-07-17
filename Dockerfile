FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_enhanced.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_enhanced.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p enhanced_data models analysis_results logs dashboard

# Set environment variables
ENV PYTHONPATH=/app
ENV REFRESH_INTERVAL=300
ENV MAX_HISTORY_DAYS=365
ENV MODEL_RETRAIN_HOURS=24

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run the application
CMD ["python", "api_server.py"]