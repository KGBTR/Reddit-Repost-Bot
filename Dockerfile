FROM python:3.9-slim-buster as base-stage

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt