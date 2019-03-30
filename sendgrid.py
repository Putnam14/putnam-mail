#!flask/bin/python
import os

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', default=None)
FROM_EMAIL = os.environ.get('FROM_EMAIL', default=None)
TO_EMAIL = os.environ.get('TO_EMAIL', default=None)

if not SENDGRID_API_KEY:
    raise ValueError("Need to set Sendgrid API Key (SENDGRID_API_KEY)")

if not FROM_EMAIL or not TO_EMAIL:
    raise ValueError("Need to set email info (FROM_EMAIL and TO_EMAIL")