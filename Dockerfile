# ---- Base image ----
FROM python:3.10-slim

# ---- System setup ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---- Create app directory ----
WORKDIR /app

# ---- Install Python dependencies ----
# First copy only requirements so Docker caching works
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---- Copy project files ----
COPY . .

# ---- Expose Cloud Run port ----
ENV PORT=8080

# ---- Start the app (FastAPI / Uvicorn) ----
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
