FROM python:3.10-slim
WORKDIR /misa


COPY requirements.txt .

# Установка системных зависимостей
RUN apt update && apt install -y \
    libsm6 \
    libxext6 \
    ffmpeg \
    libfontconfig1 \
    libxrender1 \
    libgl1 \
    libglx-mesa0 \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# Копируем и делаем исполняемым run.sh
COPY ./bots/run.sh /run.sh

ENTRYPOINT ["/bin/sh", "/run.sh"]