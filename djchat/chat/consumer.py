# consumers.py - Fixed Version
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from server.models import Server, Channel, Message 
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer): 
    async def connect(self):
        self.server_id = self.scope["url_route"]["kwargs"]["server_id"]
        self.channel_id = self.scope["url_route"]["kwargs"]["channel_id"]
        self.channel_group_name = f"server_{self.server_id}_channel_{self.channel_id}"
        
       
        if not await self.user_can_access_channel():
            await self.close()
            return
        
      
        await self.channel_layer.group_add(
            self.channel_group_name,
            self.channel_name
        )
        
        await self.accept()
        print(f"{self.scope['user'].username} joined {self.channel_group_name}")
    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        
       
        saved_msg = await self.save_message(
            server_id=self.server_id,
            channel_id=self.channel_id,
            message=message
        )
        
        
        await self.channel_layer.group_send(
            self.channel_group_name,
            {
                'type': 'channel_message',
                'message': message,
                'username': self.scope['user'].username,
                'user_id': self.scope['user'].id,
                'server_id': self.server_id,
                'channel_id': self.channel_id,
                'timestamp': str(saved_msg.timestamp) if saved_msg else None,
            }
        )
    
    async def channel_message(self, event):
    
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
            'channel_id': event['channel_id'],
            'timestamp': event['timestamp'],
        }))
    
    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.channel_group_name,
            self.channel_name
        )
    
    @database_sync_to_async
    def user_can_access_channel(self):
        user = self.scope['user']
        if not user.is_authenticated:
            return False
            
        server_id = self.scope['url_route']['kwargs']['server_id']
        channel_id = self.scope['url_route']['kwargs']['channel_id']
        

        is_member = Server.objects.filter(
            id=server_id, 
            member=user  
        ).exists()
        
        if not is_member:
            return False
        
        
        channel_exists = Channel.objects.filter(
            id=channel_id,
            server_id=server_id
        ).exists()
        
        return channel_exists
    
    @database_sync_to_async
    def save_message(self, server_id, channel_id, message):
    
        user = self.scope['user']
        channel = Channel.objects.get(id=channel_id, server_id=server_id)
        
        return Message.objects.create(
            channel=channel,
            sender=user,
            content=message,
            server_id=server_id  
        )