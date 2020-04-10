import os
import logging

version = '%BUILD_VERSION%'

environment = os.getenv('ENVIRONMENT', 'development')
database_name = os.getenv('POSTGRES_DB', 'arctendance')
database_host = os.getenv('POSTGRES_HOST', '172.17.0.3')
database_user = os.getenv('POSTGRES_USER', 'postgres')
database_pass = os.getenv('POSTGRES_PASSWORD', '')

recaptcha_secret = os.getenv('RECAPTCHA_SECRET', '')

if environment == 'development':
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)