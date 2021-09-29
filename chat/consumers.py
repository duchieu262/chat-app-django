import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Contact, Message, Chat
from django.shortcuts import get_object_or_404

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    
    def fetch_messages(self, data):
        chatId = data['chatId']
        current_chat = get_object_or_404(Chat, pk=chatId)
        messages = Chat.last_10_messages(current_chat)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        contact = data['from']
        user = User.objects.filter(username=contact)[0]
        user_contact = Contact.objects.get(user=user)
        message = Message.objects.create(contact=user_contact, content=data['message'])
        chatId = data['chatId']
        current_chat = get_object_or_404(Chat, pk=chatId)
        current_chat.messages.add(message)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id' : message.id,
            'contact': message.contact.user.username,
            'contactName': message.contact.name,
            'contactImg': message.contact.profile_pic.url,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

