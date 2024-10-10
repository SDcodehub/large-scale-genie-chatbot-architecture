import streamlit as st
import requests
import json
import re
from dotenv import load_dotenv
import os
import uuid
import logging
from logging.handlers import RotatingFileHandler

from prometheus_client import start_http_server, Counter, Histogram
import time

# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_file = '/app/logs/service_name.log'  # Replace 'service_name' with the actual service name
log_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
log_handler.setFormatter(log_formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Load environment variables
load_dotenv()

# Service URLs
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://localhost:8002/generate")
HISTORY_SERVICE_URL = os.getenv("HISTORY_SERVICE_URL", "http://localhost:8003")

st.title("Genie Chat Bot")

# Initialize session state
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = str(uuid.uuid4())
if st.session_state.current_session_id not in st.session_state.sessions:
    st.session_state.sessions[st.session_state.current_session_id] = []


def generate_unique_session_name(message, existing_names):
    # Take the first 10 characters of the message, remove non-alphanumeric characters
    base_name = re.sub(r'\W+', '', message[:10]).lower()
    if not base_name:
        base_name = "session"  # Default if message is empty or contains no alphanumeric characters
    
    # If the base_name is unique, use it
    if base_name not in existing_names:
        return base_name
    
    # If not unique, add numbers until it becomes unique
    counter = 1
    while f"{base_name}{counter}" in existing_names:
        counter += 1
    
    return f"{base_name}{counter}"


# Function to load chat history
def load_chat_history(session_id):
    logger.info(f"Loading chat history for session {session_id}")
    try:
        response = requests.get(f"{HISTORY_SERVICE_URL}/get_history/{session_id}")
        if response.status_code == 200:
            history = response.json()
            logger.info(f"Loaded {len(history)} messages for session {session_id}")
            return history
        else:
            logger.error(f"Failed to load chat history. Status code: {response.status_code}")
            st.error("Failed to load chat history.")
            return []
    except requests.RequestException as e:
        logger.error(f"Unable to load chat history. Error: {str(e)}")
        st.error("Unable to load chat history. History service might be unavailable.")
        return []

# Function to save chat history
def save_chat_history(session_id, messages):
    logger.info(f"Saving chat history for session {session_id}")
    for message in messages:
        add_message_to_history(session_id, message["role"], message["content"])
    logger.info(f"Saved {len(messages)} messages for session {session_id}")
    st.success("Chat history saved successfully!")

# Function to add message to history
def add_message_to_history(session_id, role, content):
    logger.info(f"Adding message to history for session {session_id}")
    message = {"session_id": session_id, "role": role, "content": content}
    try:
        response = requests.post(f"{HISTORY_SERVICE_URL}/add_message", json=message)
        if response.status_code != 200:
            logger.error(f"Failed to add message to history. Status code: {response.status_code}")
            st.warning("Failed to save message to history.")
    except requests.RequestException as e:
        logger.error(f"Unable to save message to history. Error: {str(e)}")
        st.warning("Unable to save message to history. History service might be unavailable.")

# Function to get LLM response
def get_llm_response(messages):
    logger.info(f"Requesting LLM response for {len(messages)} messages")
    try:
        response = requests.post(LLM_SERVICE_URL, json={"messages": messages})
        if response.status_code == 200:
            logger.info("LLM response received successfully")
            return response.json()["response"]
        else:
            logger.error(f"LLM service returned status code {response.status_code}")
            return f"Error: Received status code {response.status_code} from LLM service"
    except requests.RequestException as e:
        logger.error(f"Unable to connect to LLM service. Error: {str(e)}")
        return f"Error: Unable to connect to LLM service. {str(e)}"

# Sidebar for session management
st.sidebar.title("Chat Sessions")

if st.sidebar.button("New Session"):
    new_session_id = str(uuid.uuid4())
    st.session_state.sessions[new_session_id] = []
    st.session_state.current_session_id = new_session_id
    st.rerun()

# Display and allow selection of chat histories
for session_id in st.session_state.sessions.keys():
    session_name = session_id if len(session_id) <= 10 else session_id[:10]
    if st.sidebar.button(f"{session_name}", key=session_id):
        st.session_state.current_session_id = session_id
        st.session_state.sessions[session_id] = load_chat_history(session_id)
        st.rerun()

# Display current session name
current_session_name = st.session_state.current_session_id if len(st.session_state.current_session_id) <= 10 else st.session_state.current_session_id[:10]
st.sidebar.text(f"Current: {current_session_name}")

# Main chat interface
for message in st.session_state.sessions[st.session_state.current_session_id]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and response
if prompt := st.chat_input("What is up?"):
    logger.info(f"Received user input: {prompt[:50]}...")  # Log first 50 chars of the input
    # Rename session if it's the first message
    if not st.session_state.sessions[st.session_state.current_session_id]:
        new_session_name = generate_unique_session_name(prompt, st.session_state.sessions.keys())
        st.session_state.sessions[new_session_name] = st.session_state.sessions.pop(st.session_state.current_session_id)
        st.session_state.current_session_id = new_session_name

    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.sessions[st.session_state.current_session_id].append({"role": "user", "content": prompt})

    # Get LLM response with full conversation history
    messages = st.session_state.sessions[st.session_state.current_session_id]
    assistant_response = get_llm_response(messages)
    logger.info(f"Received assistant response: {assistant_response[:50]}...")  # Log first 50 chars of the response

    # Display assistant response
    st.chat_message("assistant").markdown(assistant_response)
    st.session_state.sessions[st.session_state.current_session_id].append({"role": "assistant", "content": assistant_response})

    # Save the new messages
    save_chat_history(st.session_state.current_session_id, 
                      [{"role": "user", "content": prompt}, 
                       {"role": "assistant", "content": assistant_response}])

    # Force a rerun to update the sidebar
    st.rerun()

# Button to save current session
if st.sidebar.button("Save Current Session"):
    save_chat_history(st.session_state.current_session_id, 
                      st.session_state.sessions[st.session_state.current_session_id])

if __name__ == "__main__":
    logger.info("Starting UI service")
    # Streamlit doesn't need explicit server start as it's handled by the streamlit command