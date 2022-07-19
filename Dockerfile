FROM python:3.9.7-slim-buster
WORKDIR /10X_instana_exporter
COPY requirements.txt .
RUN pip install --no-cache-dir --user -U -r requirements.txt
COPY / .
CMD [ "python", "main.py"]