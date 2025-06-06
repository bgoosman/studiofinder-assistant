import os
from datetime import datetime
from typing import Iterator

import streamlit as st
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from dotenv import load_dotenv

from studiofinder_tools import StudioFinderTools

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


api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")
model = os.getenv("LLM_MODEL")
local_zone = datetime.now().astimezone().tzinfo
instructions = (
    "Today is "
    + datetime.now().strftime("%Y-%m-%d")
    + " and you are a helpful assistant that can help me find a studio for rehearsal. Show me times in my timezone: "
    + str(local_zone) + ", unless I ask for a different timezone."
)
agent = Agent(
    model=OpenAIChat(id=model, api_key=api_key, base_url=api_base),
    tools=[StudioFinderTools(), ReasoningTools()],
    markdown=True,
    instructions=instructions,
    add_history_to_messages=True,
    num_history_runs=5,
    read_chat_history=True,
)


def run_studiofinder_agent(query: str):
    response_stream: Iterator[RunResponse] = agent.run(query, stream=True)
    return response_stream

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
        for response in agent.run(messages=st.session_state.messages, stream=True):
            if response.content:
                full_response += response.content
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
