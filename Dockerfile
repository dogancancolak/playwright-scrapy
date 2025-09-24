FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y \
    wget curl unzip \
    fonts-liberation fonts-unifont \
    libglib2.0-0 libnss3 libx11-6 libxcomposite1 libxdamage1 libxrandr2 \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 \
    libdrm2 libexpat1 libxkbcommon0 libxext6 libxfixes3 libpango-1.0-0 \
    libcairo2 libgbm1 libatspi2.0-0 libgdk-pixbuf-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
COPY . .
