FROM python:3.10-slim
WORKDIR /misa


COPY requirements.txt .

# Установка системных зависимостей
RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1 libglx-mesa0
RUN python -m pip install --no-cache-dir --default-timeout=300 -r requirements.txt


COPY . .
ENV PYTHONUNBUFFERED=1
# Копируем и делаем исполняемым run.sh
COPY run.sh /run.sh

ENTRYPOINT ["/bin/sh", "/run.sh"]