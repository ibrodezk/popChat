import uuid

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
# from channels import Group


class ChatConsumer(AsyncWebsocketConsumer):
    room_name = ''
    room_group_name = ''
    msgManager = AppMsgManager()
    username_group = ""
    id = -1
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # self.user = self.scope['url_route']['kwargs']['user']
        self.user = self.scope["user"]
        print(self.user)
        if (self.user.username == ""):
            self.scope["session"]["uniqKey"] = str(uuid.uuid4())
            self.id = self.scope["session"]["uniqKey"]
            self.scope["session"].save()
            self.username_group = self.scope["session"]["uniqKey"]
        else:
            self.id = self.user.id
            self.username_group = 'user_%s' % self.user.username
        await self.channel_layer.group_add(
            self.username_group,
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
        if(self.username_group == ""):
            return
        await self.channel_layer.group_discard(
            self.username_group,
            self.channel_name
        )

    async def createPopMessage(self, text_data_json):
        print("createPopMessage")
        popMessage = AppMsg(text_data_json['message'], 0, self.id)
        self.msgManager.addMsg(popMessage)
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
        self.msgManager.upvoteMsg(text_data_json['id'], self.id)
        # self.msgManager.debugPrint()
        pass

    async def refreshMessage(self):
        if(self.username_group == ""):
            return

        print("refresh message" + self.username_group)
        print(self.username_group)
        await self.channel_layer.group_send(
            self.username_group,
            {
                'type': 'refresh_message',
                'messageDict': self.msgManager.prepareEncode()
            }
        )
        # Group("user-{}".format(self.username_group)).send({
        #     "text": json.dumps({
        #         'type': 'refresh_message',
        #         'messageDict': self.msgManager.prepareEncode()
        #     })
        # })
        #self.msgManager.upvoteMsg()
        # self.channel_layer.
        pass

    async def refresh_message(self, event):
        print("refresh_message")
        dict = event['messageDict']
        print(dict)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'messageDict': dict,
            'type': "refresh_message"
        }))

    # Receive message from WebSocket
    async def receive(self, text_data):
        # await login(self.scope, User(123123))
        # await database_sync_to_async(self.scope["session"].save)()
        print(text_data)
        text_data_json = json.loads(text_data)
        print('recieve')
        if 'message' in text_data_json:
            await self.createPopMessage(text_data_json)
        if 'upvote' in text_data_json:
            await self.upvoteMessage(text_data_json)
        if 'refresh' in text_data_json:
            print("wtf is happening")
            await self.refreshMessage()

    # Receive  message from room group
    async def chat_message(self, event):
        print('chat_message')
        popMessageJson = event['popMessage']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'create_message',
            'popMessage': popMessageJson,
        }))