FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV HF_HOME=/app/.cache/huggingface
ENV TRANSFORMERS_CACHE=/app/.cache/huggingface
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    git \
    libsndfile1 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN python3 -m pip install --upgrade pip setuptools wheel \
    && python3 -m pip install \
        torch==2.6.0+cu124 \
        torchaudio==2.6.0+cu124 \
        torchvision==0.21.0+cu124 \
        --index-url https://download.pytorch.org/whl/cu124 \
    && python3 -m pip install -r /app/requirements.txt

COPY main.py /app/main.py
COPY gradio /app/gradio
COPY README.md README.fr.md HELP.md AIDE.md INSTALLATION.md /app/

RUN mkdir -p /app/audio /app/txt /app/output /app/profiles /app/.cache/huggingface

EXPOSE 7860

CMD ["python3", "gradio/app.py"]
