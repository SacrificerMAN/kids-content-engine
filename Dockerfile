FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    blender \
    ffmpeg \
    espeak-ng \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV RENDER_ENABLED=1
ENV TTS_ENABLED=1
ENV WORK_ROOT=/tmp/kids-content-engine
ENV BLENDER_BIN=blender
ENV BLENDER_TIMEOUT_SEC=3600

CMD ["uvicorn","worker:app","--host","0.0.0.0","--port","8080"]
