from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import AcceptConnection
from channels.db import database_sync_to_async
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from pills.authentication import pill_authenticator
import json


class PillNotificationConsumer(AsyncWebsocketConsumer):

    groupname = 'hub'
    async def connect(self):
        # GET ALARM PK
        try :
            self.alarm = await database_sync_to_async(self.get_pill_alarm)()
            self.alarm_id = self.alarm.pk
        except Exception :
            await self.close()
            raise AcceptConnection()

        if self.alarm_id == None :
            await self.close()
            raise AcceptConnection()

        self.room_group_name = f'pill-{self.alarm_id}'
        # self.distribute_group_name = f'pill-notify-{self.alarm_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def echo(self, event) :
        data = event['value']
        await self.send(text_data=json.dumps({'value': data}))

    async def disconnect(self, close_code=None):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    def get_pill_alarm(self) :
        return pill_authenticator.authenticate(request=self.scope)