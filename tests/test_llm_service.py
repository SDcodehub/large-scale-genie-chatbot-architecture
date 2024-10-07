import pytest
from fastapi.testclient import TestClient
from services.llm_service.app import app, LLMProvider

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_llm_provider(mocker):
    mock = mocker.Mock(spec=LLMProvider)
    app.state.llm_provider = mock
    return mock

def test_generate_response(mock_llm_provider):
    mock_llm_provider.generate_response.return_value = "Test response"

    response = client.post("/generate", json={
        "messages": [
            {"role": "user", "content": "Hello"}
        ]
    })

    assert response.status_code == 200
    assert response.json() == {"response": "Test response"}

def test_generate_response_error(mock_llm_provider):
    mock_llm_provider.generate_response.side_effect = Exception("Test error")

    response = client.post("/generate", json={
        "messages": [
            {"role": "user", "content": "Hello"}
        ]
    })

    assert response.status_code == 500
    assert "Test error" in response.json()['detail']
