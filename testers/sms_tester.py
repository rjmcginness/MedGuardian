import os
from twilio.rest import Client

# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']

# client = Client(account_sid, auth_token)


message = client.messages.create(body='Hello, World!',
                                 from_='+19897047132',
                                 to='+16038458072'
                                 )

print(message)