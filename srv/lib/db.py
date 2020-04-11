import psycopg2
import logging
from psycopg2.extras import LoggingConnection
from config import postgres_name, postgres_host, postgres_port, postgres_user, postgres_pass

logger = logging.getLogger(__name__)

conn = psycopg2.connect(
    dbname=postgres_name,
    user=postgres_user,
    password=postgres_pass,
    host=postgres_host,
    port=postgres_port)

logger.info('PostgreSQL connected')

