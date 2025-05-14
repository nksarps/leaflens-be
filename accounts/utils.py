import os
from dotenv import load_dotenv
from trycourier import Courier

load_dotenv()

client = Courier(auth_token=os.getenv('COURIER_AUTH'))


def send_confirmation_mail(email:str, first_name:str, link:str):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": os.getenv('CONFIRMATION_MAIL_TEMPLATE_ID'),
            "data": {
            "appName": "LeafLens",
            "firstName": first_name,
            "link": link,
            },
        }
    )


def send_password_reset_mail(email:str, first_name:str, link:str):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": os.getenv('PWD_RESET_MAIL_TEMPLATE_ID'),
            "data": {
            "appName": "LeafLens",
            "firstName": first_name,
            "link": link,
            },
        }
    )