import redis
import logging
from config import redis_host, redis_port

logger = logging.getLogger(__name__)

conn = redis.Redis(host=redis_host, port=redis_port, db=0)
logger.info('Redis connected')