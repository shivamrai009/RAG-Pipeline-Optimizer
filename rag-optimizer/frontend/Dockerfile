FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend/ ./frontend/

# --- FIX: Hugging Face expects Port 7860 ---
EXPOSE 7860
CMD ["streamlit", "run", "frontend/app.py", "--server.port=7860", "--server.address=0.0.0.0"]