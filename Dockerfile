FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY scripts ./scripts
COPY .env.example ./.env

ENV PYTHONPATH=/app/src
ENV DATA_DIR=/app/data
ENV DB_PATH=/app/data/safeschool.db

RUN python scripts/fetch_data.py

EXPOSE 8000
CMD ["python", "-m", "safeschool"]
