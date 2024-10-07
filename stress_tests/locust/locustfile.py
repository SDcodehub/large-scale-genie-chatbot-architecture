import json
from locust import HttpUser, task, between

class ChatbotUser(HttpUser):
    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks

    def on_start(self):
        # Simulate opening the main page
        self.client.get("/")

    @task(3)
    def send_message(self):
        # Simulate sending a message
        message = "Hello, how are you?"
        response = self.client.post("/_stcore/message", json={
            "message": message,
            "sessionId": "test_session"
        })
        if response.status_code == 200:
            # If successful, simulate receiving a response
            self.client.get("/_stcore/message")

    @task(1)
    def load_chat_history(self):
        # Simulate loading chat history
        self.client.get("/_stcore/message?history=true&sessionId=test_session")

    @task(1)
    def new_session(self):
        # Simulate starting a new chat session
        self.client.post("/_stcore/message", json={
            "newSession": True
        })

# Run with: locust -f locustfile.py
