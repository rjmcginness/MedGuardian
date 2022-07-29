FROM python:3.8

MAINTAINER Robert J McGinness

EXPOSE 8002

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONBUFFERED=1

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /services
COPY . /services

CMD ["python", "./services/med_notification.py"]

