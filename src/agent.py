from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from tools import query_ufo_faqs, query_aliens

model = ChatOpenAI(model="gpt-4o", temperature=0)
#model = ChatAnthropic(model="claude-3-5-haiku-latest")

tools = [query_ufo_faqs, query_aliens]

graph = create_react_agent(model, tools=tools)