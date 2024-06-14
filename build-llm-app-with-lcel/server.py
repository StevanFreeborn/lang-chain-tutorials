from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI
from langserve import add_routes

load_dotenv()

system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
  [("system", system_template), ("user", "{text}")]
)

model = ChatAnthropic(model="claude-3-haiku-20240307")
parser = StrOutputParser()

chain = prompt_template | model | parser

app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

add_routes(app, chain, path="/translate")

if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="localhost", port=8000)