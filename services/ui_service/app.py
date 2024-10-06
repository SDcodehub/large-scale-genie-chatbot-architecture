import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# LLM service URL
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://localhost:8001/generate")

st.title("Genie Chat Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def get_llm_response(prompt):
    try:
        response = requests.post(
            LLM_SERVICE_URL,
            json={"content": prompt},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: Received status code {response.status_code} from LLM service"
    except requests.RequestException as e:
        return f"Error: Could not connect to LLM service. {str(e)}"

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from LLM service
    with st.spinner("Thinking..."):
        response = get_llm_response(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
