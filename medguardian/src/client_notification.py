# from django.conf import settings
# from django.core.exceptions import ImproperlyConfigured
from decouple import config
from twilio.rest import Client


def load_twilio_settings() -> tuple:
    return (config('TWILIO_ACCOUNT_SID'),
            config('TWILIO_AUTH_TOKEN'),
            config('TWILIO_NUMBER'))


def send_sms(destination: str, message: str) -> None:
    twilio_sid, twilio_token, twilio_number = load_twilio_settings()
    client = Client(twilio_sid, twilio_token)

    client.messages.create(body=message,
                           from_=twilio_number,
                           to=destination)
