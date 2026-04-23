from channels.generic.websocket import WebsocketConsumer

class MyConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
    
    def receive(self, text_data = None, bytes_data = None):
        self.close()

    def disconnect(self, code):
        pass