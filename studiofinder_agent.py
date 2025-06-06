from datetime import datetime
import os
from typing import Iterator
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from studiofinder_tools import StudioFinderTools


def run_studiofinder_agent(query: str):
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")
    model = os.getenv("LLM_MODEL")
    local_zone = datetime.now().astimezone().tzinfo
    instructions = (
        "Today is "
        + datetime.now().strftime("%Y-%m-%d")
        + " and you are a helpful assistant that can help me find a studio for rehearsal. Show me times in my timezone: "
        + str(local_zone)
    )
    agent = Agent(
        model=OpenAIChat(id=model, api_key=api_key, base_url=api_base),
        tools=[StudioFinderTools(), ReasoningTools()],
        markdown=True,
        instructions=instructions,
    )
    response_stream: Iterator[RunResponse] = agent.run(query, stream=True)
    return response_stream
