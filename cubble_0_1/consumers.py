import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from core.models import Message
from django.contrib.auth.models import User 

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.friend_username = self.scope['url_route']['kwargs']['friend_username']
        # Fetch users directly from the User model
        self.user = await self.get_user(self.scope["session"]["username"])
        self.friend = await self.get_user(self.friend_username)
        if self.user and self.friend:
            self.room_group_name = f'chat_{self.friend_username}_{self.user.username}'

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save message to the database
        if self.user and self.friend:
            await self.save_message(self.user.username, self.friend.username, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, sender_username, receiver_username, message):
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        Message.objects.create(sender=sender, receiver=receiver, chat=message)

