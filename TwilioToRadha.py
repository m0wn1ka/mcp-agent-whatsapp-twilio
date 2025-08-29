import os
from dotenv import load_dotenv
load_dotenv()
from twilio.rest import Client

def send_whatsapp_message(body="Hello from Twilio!",to="whatsapp:+919390606018"):
  account_sid = os.environ["TWILIO_ACCOUNT_SID"]
  auth_token = os.environ["TWILIO_AUTH_TOKEN"]
  client = Client(account_sid, auth_token)

  message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=body,
    to=to
  )
  print(message.sid)
