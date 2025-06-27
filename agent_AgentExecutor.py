import os
import pymysql
from textwrap import dedent
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage # Role별 Message객체
from langchain_core.runnables import *
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import CSVLoader
from llm_tools.retriever import RAG_tool
from llm_tools.get_weather import get_weather_by_location_and_date
load_dotenv()
from langchain.agents import create_tool_calling_agent, AgentExecutor
from datetime import datetime

cur_date = datetime.now()

agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",f"""
당신은 문화 유산 탐사대입니다.
주요 목표는 tools를 이용해서 얻은 정보를 배경으로 사용자의 질문에 답변하세요.
현재 날짜는 {cur_date}입니다.
         
[Guidelines]
1. 대한민국의 문화유산에 대한 정보를 찾기 위해서 RAG_tool 도구를 사용하세요.
2. 날씨에 대한 정보를 찾기 위해서 get_weather_by_location_and_date 도구를 사용하세요. 지역명이 아닌, 정확한 도시명을 입력하세요.
         
각 도구의 목적과 기능을 정확하게 이해하고 각 적절한 상황에서 사용하세요.
각 도구들을 결합해서 사용자의 요청에 정확한 대답을 하세요.
항상 가장 최신의 정확한 정보를 제공하기 위해 노력하세요.
         """),
         ("human","{query}"),
         MessagesPlaceholder(variable_name="agent_scratchpad",optional=True)
    ])

tools = [RAG_tool,get_weather_by_location_and_date]

# tool_model
agent = create_tool_calling_agent(
    llm=ChatOpenAI(model_name="gpt-4.1"),
    tools=tools,
    prompt=agent_prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools
)

while True:
    query = input("\n\n >>> 쿼리를 입력하세요: ")
    if query =="!quit":
        break
    response = agent_executor.invoke({"query":query})
    print(response)

# 사용자 질문
#   필요시 SQL 쿼리문 실행
#   쿼리에 대한 결과가 ("system","contents")으로 들어옴
#       사용자 질문에 대한 결과에 대해 답을 하기에 "contents"에 정보가 모자를 경우, SQL 쿼리문 재실행
# 사용자 질문에 대한 답이 나왓을 경우, 사용자 질문 생성.
