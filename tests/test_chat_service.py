import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
import json
from unittest.mock import AsyncMock, patch
from services.chat_service.app import app, get_llm_response, websocket_endpoint

client = TestClient(app)

@pytest.fixture
def mock_websocket():
    return AsyncMock(spec=WebSocket)

@pytest.mark.asyncio
async def test_get_llm_response_success():
    with patch('httpx.AsyncClient.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"response": "Hello, how can I help you?"}
        mock_post.return_value.json = AsyncMock(return_value={"response": "Hello, how can I help you?"})
        
        response = await get_llm_response([{"role": "user", "content": "Hi"}])
        
        assert response == "Hello, how can I help you?"
        mock_post.assert_called_once_with("http://localhost:8002/generate", json={"messages": [{"role": "user", "content": "Hi"}]})

@pytest.mark.asyncio
async def test_get_llm_response_error():
    with patch('httpx.AsyncClient.post') as mock_post:
        mock_post.return_value.status_code = 500
        
        response = await get_llm_response([{"role": "user", "content": "Hi"}])
        
        assert response == "Error: Received status code 500 from LLM service"

@pytest.mark.asyncio
async def test_websocket_endpoint(mock_websocket):
    with patch('services.chat_service.app.get_llm_response') as mock_get_llm_response:
        mock_get_llm_response.return_value = "Hello, how can I help you?"
        
        mock_websocket.receive_text.return_value = json.dumps({"content": "Hi"})
        
        await websocket_endpoint(mock_websocket)
        
        mock_websocket.accept.assert_called_once()
        mock_websocket.receive_text.assert_called_once()
        mock_websocket.send_text.assert_called_once_with(json.dumps({"content": "Hello, how can I help you?"}))

@pytest.mark.asyncio
async def test_websocket_endpoint_disconnect(mock_websocket):
    mock_websocket.receive_text.side_effect = Exception("WebSocket disconnected")
    
    await websocket_endpoint(mock_websocket)
    
    mock_websocket.accept.assert_called_once()
    mock_websocket.receive_text.assert_called_once()
    assert not mock_websocket.send_text.called