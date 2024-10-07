import pytest
from unittest.mock import patch, MagicMock
import streamlit as st
from services.ui_service import app

@pytest.fixture
def mock_streamlit():
    with patch('services.ui_service.app.st') as mock_st:
        yield mock_st

def test_chat_interaction(mock_streamlit, mocker):
    mock_get_llm_response = mocker.patch('services.ui_service.app.get_llm_response', return_value="Hello, human! How can I assist you today?")
    
    # Simulate user input
    mock_streamlit.chat_input.return_value = "Hello, chatbot!"
    
    # Run the Streamlit app
    app.main()
    
    # Check if the LLM service was called
    mock_get_llm_response.assert_called_once()
    
    # Check if the response was displayed
    mock_streamlit.chat_message.assert_called_with("assistant")
    mock_streamlit.markdown.assert_called_with("Hello, human! How can I assist you today?")

def test_load_chat_history(mock_streamlit, mocker):
    mock_load_chat_history = mocker.patch('services.ui_service.app.load_chat_history', return_value=[
        {"role": "user", "content": "Test message"},
        {"role": "assistant", "content": "Test response"}
    ])
    
    # Initialize session state
    st.session_state.sessions = {}
    st.session_state.current_session_id = "test_session"
    
    app.load_chat_history()
    
    assert len(st.session_state.sessions["test_session"]) == 2
    assert st.session_state.sessions["test_session"][0]['content'] == "Test message"
    assert st.session_state.sessions["test_session"][1]['content'] == "Test response"
