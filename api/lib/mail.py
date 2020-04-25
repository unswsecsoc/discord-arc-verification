import smtplib
from datetime import timedelta
import requests

import config
import store.token

VALIDATION_MESSAGE = """
Hi {},

You (or someone else) has requested that we verify your details in order for you to participate on Discord.

Please click on {}/validations to validate your email address. When prompted, type in {}

The link will expire in {} hours.

If this wasn't you, just ignore this email.
"""

def send_validation(to: str, name: str, token: str):
    message = VALIDATION_MESSAGE.format(
			name,
			config.web_url,
			token,
			store.token.EXPIRES_VALIDATION//3600
		)
    _send_email_mailgun(to, "ARC Discord Account Verification", message)


def _send_email_mailgun(to: str, subject: str, message: str):
	return requests.post(
		f"https://api.mailgun.net/v3/{config.mailgun_domain}/messages",
		auth=("api", config.mailgun_api_key),
		data={"from": config.mailgun_from,
			"to": to,
			"subject": subject,
			"text": message})