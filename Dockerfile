FROM python:3.10-slim@sha256:2bac43769ace90ebd3ad83e5392295e25dfc58e58543d3ab326c3330b505283d
WORKDIR /misa
COPY . .
RUN pip install -r requirements.txt
CMD [ "python", "main.py" ]