FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    postgresql \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY source/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY source/. .

ENV POSTGRES_DB=minesweeper_db
ENV POSTGRES_USER=minesweeper_user
ENV POSTGRES_PASSWORD=lSlb7EkFOQ8l6VEXDcXfy3pJHhTTZY7a

RUN service postgresql start && \
    su - postgres -c "psql -c \"CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';\"" && \
    su - postgres -c "psql -c \"CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;\""

EXPOSE 1337

CMD service postgresql start && python app.py
