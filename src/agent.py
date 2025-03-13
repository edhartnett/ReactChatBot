# First we initialize the model we want to use.

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from tools import query_ufo_faqs, query_aliens

model = ChatOpenAI(model="gpt-4o", temperature=0)
#model = ChatAnthropic(model="claude-3-5-haiku-latest")


# For this tutorial we will use custom tool that returns pre-defined values for weather in two cities (NYC & SF)

from typing import Literal

from langchain_core.tools import tool


@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


tools = [get_weather, query_ufo_faqs, query_aliens]


# Define the graph

from langgraph.prebuilt import create_react_agent

graph = create_react_agent(model, tools=tools)

# def print_stream(stream):
#     for s in stream:
#         message = s["messages"][-1]
#         if isinstance(message, tuple):
#             print(message)
#         else:
#             message.pretty_print()

# inputs = {"messages": [("user", "what is the weather in sf")]}
# print_stream(graph.stream(inputs, stream_mode="values"))