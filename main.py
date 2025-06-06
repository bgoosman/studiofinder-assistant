from datetime import datetime
import streamlit as st
from studiofinder_agent import run_studiofinder_agent
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="StudioFinder Assistant",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ StudioFinder Assistant")
st.markdown("""
This assistant helps you find and evaluate recording studios based on your needs.
Simply describe what you're looking for, and the assistant will help you find the perfect studio!
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What kind of studio are you looking for?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream the response
        for response in run_studiofinder_agent(prompt):
            if response.content:
                full_response += response.content
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
