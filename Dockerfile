FROM python:3.11-slim

WORKDIR /fastapi

COPY . /fastapi

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000

ENV NAME World

WORKDIR /fastapi/src/app

CMD uvicorn main:app --host '0.0.0.0'
