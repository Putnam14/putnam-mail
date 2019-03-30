#!flask/bin/python
import os
import requests

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', default=None)
FROM_EMAIL = os.environ.get('FROM_EMAIL', default=None)
TO_EMAIL = os.environ.get('TO_EMAIL', default=None)

if not SENDGRID_API_KEY:
    raise ValueError("Need to set Sendgrid API Key (SENDGRID_API_KEY)")

if not FROM_EMAIL or not TO_EMAIL:
    raise ValueError("Need to set email info (FROM_EMAIL and TO_EMAIL")

sendgrid_url = 'https://api.sendgrid.com/v3/mail/send'

def build_request_body(email):
    from_email = email['email']
    name = email['name']
    subject = email['subject']
    body = email['body']
    if from_email == "":
        from_email = FROM_EMAIL
    if name == "":
        name = "Anonymous"
    if subject == "":
        subject = "Portfolio contact form message"
    req_body = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": TO_EMAIL
                    }
                ],
                "subject": subject
            }
        ],
        "from": {
            "email": from_email,
            "name": name
        },
        "content": [
            {
                "type": "text/plain",
                "value": body
            }
        ]
    }
    return req_body

def send_mail(email):
    email_body = build_request_body(email)
    return email_body
