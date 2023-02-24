FROM python:3.10-slim
WORKDIR /misa
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ADD run.sh /
ENTRYPOINT ["/bin/sh", "/run.sh"]

