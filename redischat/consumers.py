import json
from pprint import pprint

import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message
from django.conf import settings as django_settings

DB_REDIS = django_settings.DB_REDIS


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Obtains the 'room_name' parameter from the URL route
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """
        Receive message from websocket and send to target room group
        """
        data_json = json.loads(text_data)
        message = data_json['message']
        username = data_json['username']
        room = data_json['room']

        # TODO : edit this data saving
        await self.save_message(username, room, message)
        # await self.redis_save_message(username, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, data):
        """
        Receive message from room group
        """
        message = data['message']
        username = data['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        Message.objects.create(
            username=username,
            room=room,
            content=message,
        )

    @sync_to_async
    def redis_save_message(self, username, room_id, message):
        """
        TODO = faire une descrpition
        tools
        """
        user_id = self.redis_get_room_user_id_by_name(room_id, username)
        DB_REDIS.hmset(f"room:{self.room_id}:message", {
            "content": message,
            "sender": username,
        })
        DB_REDIS.hset(f"room:{self.room_id}:messages", username, user_id)
        DB_REDIS.hincrby(f"room:{room_id}", "last_message_id", 1)

    @sync_to_async
    def redis_get_room_user_id_by_name(self, room_id, username):
        """
        TODO
        """
        try:
            result = DB_REDIS.hget(f"room:{room_id}:users", username)
            return result if result else None
        except redis.exceptions.ConnectionError as e:
            raise e