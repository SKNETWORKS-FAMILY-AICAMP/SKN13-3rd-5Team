import os
import pymysql
from textwrap import dedent
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage # Role별 Message객체
from langchain_core.runnables import *
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

system_prompt = """
당신은 한국 문화유산 전문가입니다.
한국 문화유산에 관한 데이터는 대부분 MySQL에 저장되어 있습니다.
한국 문화유산에 대한 질문이 들어온다면, MySQL DB에 저장되어 있는 데이터를 기반으로 사용자의 질문에 답변해주세요.
MySQL DB에 있는 데이터로 답변할 수 없을 경우, 웹 서핑 툴을 사용하여 답변하세요.
"""

template = """
[Instruction]

"""


# 사용자 질문
#   필요시 SQL 쿼리문 실행
#   쿼리에 대한 결과가 ("system","contents")으로 들어옴
#       사용자 질문에 대한 결과에 대해 답을 하기에 "contents"에 정보가 모자를 경우, SQL 쿼리문 재실행
# 사용자 질문에 대한 답이 나왓을 경우, 사용자 질문 생성.

class ChatBot(Runnable):
    def __init__(self):
        super().__init__()
        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")
        self.user = os.getenv("USER")
        self.pw = os.getenv("PASS")
        self.model = ChatOpenAI(model_name='gpt-4o-mini')
        self.model.invoke(system_prompt)
        self.prompt_template = PromptTemplate(template=template)
        self.parser = StrOutputParser()
        self.history = InMemoryChatMessageHistory()

        self.chain = self.prompt_template | self.function_call() | self.parser

    def create_response(self,query):
        return self.chain.invoke(query)

    @chain
    def function_call(self,query):  # 여기서 query는 prompt_template을 거친 query
        response = self.model.invoke(query)
        if response[0] == "tools":
            response = self.use_tool(response)

        print(response)

    def use_tool(self,response):
        tool_response = use_tool(response)
        new_response = model.invoke(tool_response)

        if new_response[0]=="tools":
            use_tool(new_response)
        else:
            return new_response