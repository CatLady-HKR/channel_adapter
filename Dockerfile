FROM python:3.11-slim

# Install system dependencies for audio processing and TTS
RUN apt-get update && apt-get install -y \
    ffmpeg \
    flac \
    portaudio19-dev \
    python3-dev \
    gcc \
    espeak \
    espeak-data \
    libespeak1 \
    libespeak-dev \
    festival \
    alsa-utils \
    curl \
    pulseaudio \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
