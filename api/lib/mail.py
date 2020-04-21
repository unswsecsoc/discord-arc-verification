import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import timedelta
from config import mailgun_from, mailgun_domain, mailgun_api_key
import requests
from config import web_url

VALIDATION_MESSAGE = """
Hi {},

You (or someone else) has requested that we verify your details in order for you to participate on Discord.

Please click on {}/validations to validate your email address. When prompted, type in {}

The link will expire in {} hours.

If this wasn't you, just ignore this email.
"""

def send_validation(to: str, name: str, token: str, expires: timedelta):
    message = VALIDATION_MESSAGE.format(name, web_url, token, expires.seconds/3600)
    _send_email_mailgun(to, "ARC Discord Account Verification", message)


def _send_email_mailgun(to: str, subject: str, message: str):
	return requests.post(
		f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
		auth=("api", mailgun_api_key),
		data={"from": mailgun_from,
			"to": to,
			"subject": subject,
			"text": message})