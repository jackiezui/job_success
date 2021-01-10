# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import os
from django.conf import settings

BASH_PATH = os.path.join(settings.STATIC_DIR, 'bash')


class CommandConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        pass

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        filename = f"output_{command}.txt"
        if os.path.exists(os.path.join(BASH_PATH, filename)):
            os.remove(os.path.join(BASH_PATH, filename))
            self.send(text_data=json.dumps({'is_existed': 'Yes'}))
