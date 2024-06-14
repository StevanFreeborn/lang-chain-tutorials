import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatAnthropic(model="claude-3-haiku-20240307")
parser = StrOutputParser()

messages = [
  SystemMessage(content="Translate the following from English into Italian"),
  HumanMessage(content="hi!"),
]

chain = model | parser

res = chain.invoke(messages)

print(res)