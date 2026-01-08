# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Build Backend & Runtime
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Backend Code
COPY backend ./backend

# Copy Built Frontend Assets (for serving static files if needed, or separate container)
# For this MVP, we assume we might serve static files from FastAPI or use a separate Nginx.
# Let's keep it simple: Monolithic container for now, or just Backend.
# Given the project structure, it's a separate React app. 
# Usually, MLOps means separate containers. 
# Let's stick to a Python Backend container for now, as that's the core "Engine".
# I'll create a separate Dockerfile structure or just one for the backend service.

# Let's do a pure Backend Dockerfile for the API service.
# The frontend would typically be served via Nginx or Vercel/Netlify.
# But for "Platform Engineering", a docker-compose often spins up both.
# I will rewrite this to be just the Backend Service, and docker-compose will handle the rest.

# --- REVISED BACKEND DOCKERFILE ---
# Keep it simple, focus on the API.

ENV PYTHONPATH=/app
ENV PORT=8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
