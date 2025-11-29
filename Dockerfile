FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY api/ api/
COPY src/ src/
# Create data directory for cache
RUN mkdir -p /tmp/data

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "api.index:app", "--host", "0.0.0.0", "--port", "8000"]
