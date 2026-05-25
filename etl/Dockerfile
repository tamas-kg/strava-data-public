FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install OS-level dependencies (optional, but helpful for debugging)
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY bronze_load.py .
COPY tokens.json .
COPY src/ src/

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default command
# CMD ["python", "bronze_load.py"]
CMD ["sleep", "infinity"]