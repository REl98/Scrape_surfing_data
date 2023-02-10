import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC0422ed9532ca75aefcee3f356f27635f'
auth_token = '2fb12d59a35125286530c4f4e2f83660'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Skinny bitch !!!",
                     from_='+18086466857',
                     to='+972546718261'
                 )

print(message.sid)