from langchain_anthropic import ChatAnthropic
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

store = {"configurable": {"session_id": "1"}}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
  if session_id not in store:
    store[session_id] = ChatMessageHistory()
  return store[session_id]

model = ChatAnthropic(model="claude-3-haiku-20240307")

with_message_history = RunnableWithMessageHistory(model, get_session_history)

config = {"configurable": {"session_id": "1"}}

while True:
  user_input = input("You: ")
  message = HumanMessage(content=user_input)
  response = with_message_history.invoke(message, config)
  print("Bot:", response.content)