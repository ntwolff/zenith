import redis
from app.config.settings import settings

RedisClient = redis.Redis(
    host=settings.redis.redis_host,
    port=settings.redis.redis_port,
    db=settings.redis.redis_db,
    password=settings.redis.redis_password
)