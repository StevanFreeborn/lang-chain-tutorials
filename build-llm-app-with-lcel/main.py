import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()

model = ChatAnthropic(model="claude-3-haiku-20240307")

