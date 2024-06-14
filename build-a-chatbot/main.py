from langchain_anthropic import ChatAnthropic
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough


load_dotenv()

store = {"configurable": {"session_id": "1"}}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
  if session_id not in store:
    store[session_id] = ChatMessageHistory()
  return store[session_id]

def filter_messages(messages, k=10):
  return messages[-k:]

model = ChatAnthropic(model="claude-3-haiku-20240307")

prompt = ChatPromptTemplate.from_messages([
  ("system", "You are a helpful assistant. Answer all questions to the best of your ability in {language}."), 
  MessagesPlaceholder(variable_name="messages")
])

chain = (
  RunnablePassthrough.assign(messages=lambda x: filter_messages(x["messages"]))
  | prompt
  | model
)

chain = prompt | model

with_message_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="messages")

config = {"configurable": {"session_id": "1"}}

while True:
  user_input = input("You: ")
  message = HumanMessage(content=user_input)
  print("Bot: ", end="")
  for r in with_message_history.stream(
    { "messages": HumanMessage(content=user_input), "language": "English"},
    config=config
  ):
    print(r.content, end="")
  print()