FROM python:3.8

EXPOSE 8002

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONBUFFERED=1

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# RUN mkdir /home/medguardian/data
WORKDIR /home/medguardian/data
COPY ./data /home/medguardian/data

WORKDIR /services
COPY . /services

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# CMD ["python", "med_notification.py"]

