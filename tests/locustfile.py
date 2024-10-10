import time
import json
import random
from locust import HttpUser, task, between
from locust.contrib.fasthttp import FastHttpUser
from locust.exception import RescheduleTask
from websocket import create_connection

class ChatBotUser(FastHttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        self.ws = None
        self.session_id = f"locust_test_{random.randint(1000, 9999)}"
        self.chat_service_host = "127.0.0.1:8000"
        self.history_service_host = "http://127.0.0.1:8003"

    def on_stop(self):
        if self.ws:
            self.ws.close()

    def connect_websocket(self):
        if not self.ws:
            try:
                self.ws = create_connection(f"ws://{self.chat_service_host}/ws")
            except Exception as e:
                print(f"WebSocket connection failed: {e}")
                raise RescheduleTask()

    @task(3)
    def send_chat_message(self):
        self.connect_websocket()
        message = f"This is a test message {random.randint(1, 1000)}"
        try:
            self.ws.send(json.dumps({"content": message}))
            response = self.ws.recv()
            response_data = json.loads(response)
            if "content" not in response_data:
                print(f"Unexpected response: {response_data}")
        except Exception as e:
            print(f"WebSocket communication failed: {e}")
            self.ws = None  # Reset the connection
            raise RescheduleTask()

    @task(1)
    def save_chat_history(self):
        message = {
            "session_id": self.session_id,
            "role": "user",
            "content": f"Test message for history {random.randint(1, 1000)}"
        }
        with self.client.post(f"{self.history_service_host}/add_message", json=message, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to save message: {response.text}")

    @task(1)
    def get_chat_history(self):
        with self.client.get(f"{self.history_service_host}/get_history/{self.session_id}", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get history: {response.text}")