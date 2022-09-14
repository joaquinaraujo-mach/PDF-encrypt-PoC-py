FROM python:3.9-slim

RUN mkdir -p /opt/app
COPY requirements.txt /opt/app/
COPY src/ /opt/app/src

WORKDIR /opt/app
RUN pip install -r requirements.txt --cache-dir /opt/app/__pycache__

ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV AWS_SESSION_TOKEN=""

CMD [ "python", "src/run.py" ]