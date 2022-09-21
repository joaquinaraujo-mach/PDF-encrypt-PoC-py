FROM python:3.9-slim

WORKDIR /opt/app

COPY ["requirements.txt", "."]
COPY ["src", "."]

RUN pip install -r requirements.txt --cache-dir /opt/app/__pycache__
