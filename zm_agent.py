import os
from dotenv import load_dotenv
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.document_loaders import CSVLoader
from llm_tools.retriever import RAG_tool
from llm_tools.get_weather import get_weather_by_location_and_date
from langchain.agents import create_tool_calling_agent, AgentExecutor

from chat_history_manager import ChatHistoryManager

load_dotenv()

chat_history = ChatHistoryManager()
cur_date = datetime.now()

agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", f"""
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
        ("human", "{query}"),
        MessagesPlaceholder(variable_name="agent_scratchpad", optional=True)
    ]
)

tools = [RAG_tool, get_weather_by_location_and_date]

agent = create_tool_calling_agent(
    llm=ChatOpenAI(model_name="gpt-4.1"),
    tools=tools,
    prompt=agent_prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools
)

def pretty_print_response(query, response):
    print("\n[사용자] " + query)
    if isinstance(response, dict) and "output" in response:
        print("[챗봇] " + response["output"].strip())
    else:
        print("[챗봇] " + str(response).strip())
    print("-" * 40)

def print_history(chat_history):
    print("\n=== 대화 히스토리 ===")
    for msg in chat_history.get_history():
        role = getattr(msg, "type", getattr(msg, "role", "unknown"))
        if role == "human":
            print("[사용자] " + msg.content)
        elif role == "ai":
            print("[챗봇] " + msg.content)
        else:
            print(f"[{role}] {msg.content}")
    print("=" * 40)

def get_user_questions_from_history(chat_history):
    return [msg.content for msg in chat_history.get_history() if getattr(msg, "type", getattr(msg, "role", "")) == "human"]

if __name__ == "__main__":
    while True:
        query = input("\n\n >>> 쿼리를 입력하세요: ")
        if query == "!quit":
            break
        if query == "!history":
            print_history(chat_history)
            continue

        # "내가 뭐뭐 물어봤더라?" 같은 질문에 대해 사용자 질문 목록 출력
        if "뭐뭐 물어봤" in query or "내가 뭐 물어봤" in query:
            user_questions = get_user_questions_from_history(chat_history)
            if user_questions:
                print("\n[챗봇] 지금까지 하신 질문 목록입니다:")
                for i, q in enumerate(user_questions, 1):
                    print(f"  {i}. {q}")
            else:
                print("\n[챗봇] 아직 남기신 질문이 없습니다.")
            print("-" * 40)
            chat_history.add_user_message(query)
            chat_history.add_assistant_message("지금까지 하신 질문 목록을 안내해드렸습니다.")
            continue

        chat_history.add_user_message(query)

        response = agent_executor.invoke({
            "query": query,
            "agent_scratchpad": chat_history.get_history()
        })

        pretty_print_response(query, response)

        if isinstance(response, dict) and "output" in response:
            chat_history.add_assistant_message(response["output"])
        else:
            chat_history.add_assistant_message(str(response))
