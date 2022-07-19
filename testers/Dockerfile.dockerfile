FROM python:3.9.7-alpine

RUN mkdir /usr/src/alertservice
WORKDIR /usr/src/alertservice
COPY ./requirements.txt .

RUN python -m pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . .