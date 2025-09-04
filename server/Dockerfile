FROM python:3.10-slim
WORKDIR /misa


COPY ./server/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем все папки в /misa
COPY Front_layer/ ./Front_layer/
COPY Core_layer/ ./Core_layer/

COPY Deep_layer/ ./Deep_layer/
COPY server/ .

# Копируем и делаем исполняемым run.sh
COPY ./server/run.sh /run.sh

ENTRYPOINT ["/bin/sh", "/run.sh"]