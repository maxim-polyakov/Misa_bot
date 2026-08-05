FROM python:3.11-slim
WORKDIR /misa


COPY requirements.txt .

# Установка системных зависимостей
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        libfontconfig1 \
        libgl1 \
        libsm6 \
        libxext6 \
        libxrender1 \
    && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --no-cache-dir --default-timeout=300 -r requirements.txt


COPY . .
ENV PYTHONUNBUFFERED=1
# Копируем и делаем исполняемым run.sh
COPY run.sh /run.sh

ENTRYPOINT ["/bin/sh", "/run.sh"]