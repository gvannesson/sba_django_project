# chat/consumers.py
import json
from datetime import datetime
from random import randint

from channels.generic.websocket import AsyncWebsocketConsumer


usernames = ["Clodo Maskay", "SuperKuvett"]
chatlog = ['XbYwQzt', 'TjklzPDqpL', 'VrgtMzsF', 'QjwpKLfdm', 'zXprTqFk', 'LsjDbPZW', 
 'MjXqzFLkp', 'BfZtWMpk', 'TpLkzJqXF', 'QxTpzMkLf', 'FLjXqzTPm', 'PzTkqXFLm', 
 'LzTqXPFmJ', 'zQxTjFLPk', 'XjTqzPMkL', 'ZpTqLXjFM', 'TkqLXzJPF', 'qTpXjZFLM', 
 'JpTkXqZFL', 'TqXjZPMkL']

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        
        #Join room groupe
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)       
   
        
        await self.accept()
        
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "load.log", "messages": chatlog}
        )

    async def disconnect(self, close_code):
        #Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    #Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        #send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )
        
    async def chat_message(self, event):
        message = usernames[randint(0,1)]+ " ("+str(datetime.now().hour)+":"+str(datetime.now().minute)+") : " + event["message"]
        
        #send message to websocket
        await self.send(text_data=json.dumps({"message": message}))
        
    async def load_log(self, event):
        # print(event["messages"])
        log = ""
        for message in event["messages"]:
            log += usernames[randint(0,1)]+ " ("+str(datetime.now().hour)+":"+str(datetime.now().minute)+") : " + message+"\r\n"
        # print("PRINT : " + log)
        
        await self.send(text_data=json.dumps({"log":log}))