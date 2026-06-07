FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PostgreSQL and building packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Hugging Face Spaces uses port 7860
EXPOSE 7860

# Run migrations, seed the database, and start the app
CMD ["sh", "-c", "alembic upgrade head && python seeds/seed_users.py && uvicorn main:app --host 0.0.0.0 --port 7860"]
