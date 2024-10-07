from fastapi.testclient import TestClient
from services.history_service.app import app, chat_history

client = TestClient(app)

def test_add_message():
    response = client.post("/add_message", json={
        "session_id": "test_session",
        "role": "user",
        "content": "Test message"
    })
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

def test_get_history():
    # Clear the history first
    chat_history.clear()
    
    # Add a message
    client.post("/add_message", json={
        "session_id": "test_session",
        "role": "user",
        "content": "Test message"
    })

    # Retrieve the history
    response = client.get("/get_history/test_session")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["content"] == "Test message"

def test_get_nonexistent_history():
    response = client.get("/get_history/nonexistent_session")
    assert response.status_code == 404
