import psycopg2
import logging
from psycopg2.extras import LoggingConnection
from config import database_name, database_host, database_user, database_pass

logger = logging.getLogger(__name__)

conn = psycopg2.connect(
    dbname=database_name,
    user=database_user,
    password=database_pass,
    host=database_host)

logger.info('PostgreSQL connected')

