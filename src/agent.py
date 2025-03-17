from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from tools import query_ufo_faqs, query_aliens

model = ChatOpenAI(model="gpt-4o", temperature=0)
#model = ChatAnthropic(model="claude-3-5-haiku-latest")

tools = [query_ufo_faqs, query_aliens]
prompt = '''
You are a UFOologist. You are certain that UFOs are alien spaceships,and that the government is keeping them hidden. 
You believe every aspect of reported UFOs and encounters with aliens.
Answer questions about UFOs and aliens.
'''

graph = create_react_agent(model, tools=tools, prompt=prompt)
