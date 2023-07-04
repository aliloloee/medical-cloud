from django.conf import settings
import redis
import os
# from decouple import config



class Redis() :
    def __init__(self) :
        if settings.DEBUG :
            self.redis = redis.Redis(host='localhost', port=6379, db=1)

        if not settings.DEBUG :
            redis_port = os.getenv('REDIS_PORT', 'redis port not found')
            redis_host = os.getenv('REDIS_HOST', 'redis host not found')
            redis_pass = os.getenv('REDIS_PASSWORD', 'redis password not found')
            self.redis = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=1, 
                password=redis_pass
                )


    def cache_activation_key(self, key, value) :
        self.redis.set(
            str(key),
            str(value),
            ex=settings.DEVICE_ACTIVATION_CODE_EXPIRATION_TIMESTAMP,
            nx=True
            )

    def check_key_value_validity(self, key, value) :
        try :
            db_value = self.redis.get(str(key)).decode("utf-8")
        except :
            return False
        return value == db_value 

    def check_key_existance(self, key) :
        try :
            self.redis.get(str(key)).decode("utf-8")
        except :
            return False
        return True

    def delete_key(self, key) :
        self.redis.delete(str(key))

    def _db(self) :
        return self.redis

    # def save_to_stream(self, stream, fields) :
    #     self.redis.xadd(stream, fields)


HUBCACHE = Redis()