from celery import shared_task

from devices.models import Record
from hub.redis_conf import HUBCACHE



@shared_task
def export_from_redis_to_db(*args, **kwargs) :
    # Send activation link
    record_id  = kwargs.get('record_id', None)
    queue_name = kwargs.get('queue_name', None)
    queue_size = kwargs.get('queue_size', None)

    # redis
    redis = HUBCACHE._db()

    rec = Record.objects.get(id=record_id)
    queue = redis.lrange(queue_name, -queue_size, queue_size)

    rec.data = rec.data + [int(x.decode('UTF8')) for x in queue] 
    rec.save()

    HUBCACHE.delete_key(queue_name)

    # load record, and redis_queue | export queue to record(append) | delete the queue from redis