from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import AcceptConnection
from channels.db import database_sync_to_async
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from devices.authentication import device_authenticator
from devices.models import Record
from hub.redis_conf import HUBCACHE
from client.tasks import export_from_redis_to_db
import json


class LiveDataDistributer(AsyncWebsocketConsumer) :

    groupname = 'hub'
    async def connect(self):
        # GET DEVICE PK
        try :
            self.device = await database_sync_to_async(self.get_device)()
            self.device_pk = self.device.pk
        except Exception :
            await self.close()
            raise AcceptConnection()

        if self.device_pk == None :
            await self.close()
            raise AcceptConnection()

        # ADD TO GROUP
        self.room_group_name = f'distribute-{self.device_pk}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # ACCEPT CONNECTION
        await self.accept()

    async def disconnect(self, close_code=None):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    def get_device(self) :
        return device_authenticator.authenticate(request=self.scope, protocol='ws')

    async def echo(self, event) :
        val = int(event['value'])
        await self.send(text_data=json.dumps({'value': val}))



class LiveDataConsumer(AsyncWebsocketConsumer):

    groupname = 'hub'
    async def connect(self):
        # GET DEVICE PK
        try :
            self.device = await database_sync_to_async(self.get_device)()
            self.device_pk = self.device.pk
        except Exception :
            await self.close()
            raise AcceptConnection()

        if self.device_pk == None :
            await self.close()
            raise AcceptConnection()
        
        # CREATE A RECORD
        self.record = await database_sync_to_async(self.create_record)()
        
        # GET REDIS DATABASE
        self.redis = HUBCACHE._db()
        self.queue_size = 100
        self.queue_name = f'queue:{self.device_pk}:{self.record.pk}' 
        self.counter = 0

        self.room_group_name = f'publish-{self.device_pk}'
        self.distribute_group_name = f'distribute-{self.device_pk}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None):
        if text_data :
            val = json.loads(text_data)['value']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'processing',
                    'value': val
                }
            )

            await self.channel_layer.group_send(
                self.distribute_group_name,
                {
                    'type': 'echo',
                    'value': val
                }
            )

    async def processing(self, event) :
        val = int(event['value'])
        await self.add_to_db(val)
        # await self.send(text_data=json.dumps({'value': val}))


    async def disconnect(self, close_code=None):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    def get_device(self) :
        return device_authenticator.authenticate(request=self.scope, protocol='ws')

    def create_record(self) :
        kw = {
            'device':self.device,
            'data':[]
        }
        try :
            record_name = dict(self.scope['headers'])[settings.DEVICE_HEADER_RECORD_NAME.encode('utf-8')].decode('utf-8')
            if record_name.strip() == '' :
                record_name = None
        except : 
            record_name = None

        if record_name != None :
            kw['name'] = record_name

        return Record.objects.create(**kw)

    async def add_to_db(self, value) :
        self.redis.rpush(self.queue_name, value)
        len = self.redis.llen(self.queue_name)
        if len == self.queue_size :
            prime_queue = f'{self.queue_name}-prime:{self.counter}'

            self.redis.rename(self.queue_name, prime_queue)
            export_from_redis_to_db.apply_async(kwargs={
                                'record_id': str(self.record.pk),
                                'queue_name': prime_queue,
                                'queue_size': self.queue_size,
                                })
            self.counter = self.counter + 1

            HUBCACHE.delete_key(self.queue_name)
