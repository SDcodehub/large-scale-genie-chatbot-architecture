import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os
import uuid

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

# Function to load chat history
def load_chat_history(session_id):
    try:
        response = requests.get(f"{HISTORY_SERVICE_URL}/get_history/{session_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to load chat history.")
            return []
    except requests.RequestException:
        st.error("Unable to load chat history. History service might be unavailable.")
        return []

# Function to save chat history
def save_chat_history(session_id, messages):
    for message in messages:
        add_message_to_history(session_id, message["role"], message["content"])
    st.success("Chat history saved successfully!")

# Function to add message to history
def add_message_to_history(session_id, role, content):
    message = {"session_id": session_id, "role": role, "content": content}
    try:
        requests.post(f"{HISTORY_SERVICE_URL}/add_message", json=message)
    except requests.RequestException:
        st.warning("Unable to save message to history. History service might be unavailable.")

# Function to get LLM response
def get_llm_response(messages):
    try:
        response = requests.post(LLM_SERVICE_URL, json={"messages": messages})
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: Received status code {response.status_code} from LLM service"
    except requests.RequestException as e:
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
    if st.sidebar.button(f"Session {session_id[:8]}...", key=session_id):
        st.session_state.current_session_id = session_id
        st.session_state.sessions[session_id] = load_chat_history(session_id)
        st.rerun()

# Display current session ID
st.sidebar.text(f"Current Session: {st.session_state.current_session_id[:8]}...")

# Main chat interface
for message in st.session_state.sessions[st.session_state.current_session_id]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and response
if prompt := st.chat_input("What is up?"):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.sessions[st.session_state.current_session_id].append({"role": "user", "content": prompt})

    # Get LLM response with full conversation history
    messages = st.session_state.sessions[st.session_state.current_session_id]
    assistant_response = get_llm_response(messages)

    # Display assistant response
    st.chat_message("assistant").markdown(assistant_response)
    st.session_state.sessions[st.session_state.current_session_id].append({"role": "assistant", "content": assistant_response})

    # Save the new messages
    save_chat_history(st.session_state.current_session_id, 
                      [{"role": "user", "content": prompt}, 
                       {"role": "assistant", "content": assistant_response}])

# Button to save current session
if st.sidebar.button("Save Current Session"):
    save_chat_history(st.session_state.current_session_id, 
                      st.session_state.sessions[st.session_state.current_session_id])