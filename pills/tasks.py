from celery import shared_task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import json


@shared_task
def send_pill_notification(*args, **kwargs) :
    pill     = kwargs.get('pill', None)
    alarm_id = kwargs.get('alarm-id', None)
    user     = kwargs.get('user', None)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"pill-{alarm_id}",
        {
            "type": "echo",
            "value": json.dumps({'pill':pill, 'user':user})
        }
        )

    print(f'Consumption of {pill} for user {user}')