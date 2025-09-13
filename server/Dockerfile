FROM python:3.10-slim
WORKDIR /misa


COPY requirements.txt .

RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx

RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# Копируем и делаем исполняемым run.sh
COPY run.sh /run.sh

ENTRYPOINT ["/bin/sh", "/run.sh"]