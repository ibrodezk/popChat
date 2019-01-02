from asgiref.sync import async_to_sync
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json
# chat/consumers.py
import json
from channels.auth import login
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from common.AppMsgManager import AppMsgManager
from common.AppMsg import AppMsg


class ChatConsumer(AsyncWebsocketConsumer):
    room_name = ''
    room_group_name = ''
    msgManager = AppMsgManager()

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # self.user = self.scope['url_route']['kwargs']['user']
        self.user = self.scope["user"]
        print(self.user)
        if (self.user.username != ""):
            username_group = 'user_%s' % self.user.username
            await self.channel_layer.group_add(
                username_group,
                self.channel_name
            )
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

    async def createPopMessage(self, text_data_json):
        print("createPopMessage")
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

    async def upvoteMessage(self, text_data_json):
        self.msgManager.upvoteMsg(text_data_json['id'])
        # self.msgManager.debugPrint()
        pass

    async def refreshMessage(self, text_data_json):
        #self.msgManager.upvoteMsg()
        # self.channel_layer.
        pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        # await login(self.scope, User(123123))
        # await database_sync_to_async(self.scope["session"].save)()
        # print(self.scope)
        text_data_json = json.loads(text_data)
        print('recieve')
        if 'message' in text_data_json:
            await self.createPopMessage(text_data_json)
        if 'upvote' in text_data_json:
            await self.upvoteMessage(text_data_json)
        if 'refresh' in text_data_json:
            await self.refreshMessage(text_data_json)

    # Receive  message from room group
    async def chat_message(self, event):
        print('chat_message')
        text = event['popMessage']['msg']
        popMessage = AppMsg(text, 0)
        self.msgManager.addMsg(popMessage)
        # Send message to WebSocket
        print(popMessage)
        await self.send(text_data=json.dumps({
            'popMessage': popMessage.prepareEncode(),
        }))