from asgiref.sync import async_to_sync
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json
# chat/consumers.py
import json

from common.AppMsg import AppMsg


class ChatConsumer(AsyncWebsocketConsumer):
    room_name = ''
    room_group_name = ''
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("recieve")
        text_data_json = json.loads(text_data)
        popMessage = AppMsg(text_data_json['message'], 0)
        print(str(popMessage))
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'popMessage': popMessage.prepareEncode()
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print('chat_message')
        text = event['popMessage']
        popMessage = AppMsg(text, 0)

        # Send message to WebSocket
        print(popMessage)
        await self.send(text_data=json.dumps({
            'popMessage': popMessage.prepareEncode()
        }))