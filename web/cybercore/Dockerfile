FROM python:3.11-slim

COPY source/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY source/. /app
WORKDIR /app

USER root
EXPOSE 1337
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1337"]