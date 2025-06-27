import os
from dotenv import load_dotenv
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from llm_tools.retriever import RAG_tool
from llm_tools.get_weather import get_weather_by_location_and_date
from chat_history_manager import SessionChatHistoryManager

load_dotenv()

# 세션 매니저 생성
session_manager = SessionChatHistoryManager()
session_id = "default_session"  # 실제 서비스에서는 사용자별 세션 ID 필요
session_manager.create_session(session_id)

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

def print_history(session_id):
    print("\n=== 대화 히스토리 ===")
    history = session_manager.get_history(session_id)
    for msg in history:
        role = getattr(msg, "type", getattr(msg, "role", "unknown"))
        if role == "human":
            print("[사용자] " + msg.content)
        elif role == "ai":
            print("[챗봇] " + msg.content)
        else:
            print(f"[{role}] {msg.content}")
    print("=" * 40)

def get_user_questions_from_history(session_id):
    history = session_manager.get_history(session_id)
    return [msg.content for msg in history if getattr(msg, "type", getattr(msg, "role", "")) == "human"]

def handle_show_history_command(session_manager, session_id, query):
    """
    사용자가 대화 히스토리 요청 시 세션에서 직접 히스토리를 출력하는 함수
    """
    history = session_manager.get_history(session_id)
    if history:
        print("\n[챗봇] 지금까지 대화 내용입니다:")
        for i, msg in enumerate(history, 1):
            role = getattr(msg, "type", getattr(msg, "role", "unknown"))
            if role == "human":
                print(f"{i}. [사용자] {msg.content}")
            elif role == "ai":
                print(f"{i}. [챗봇] {msg.content}")
            else:
                print(f"{i}. [{role}] {msg.content}")
    else:
        print("\n[챗봇] 아직 대화 내용이 없습니다.")
    # 히스토리 출력 후, 히스토리에도 기록
    session_manager.add_user_message(session_id, query)
    session_manager.add_assistant_message(session_id, "지금까지 대화 내용을 안내해드렸습니다.")

if __name__ == "__main__":
    while True:
        query = input("\n\n >>> 쿼리를 입력하세요: ")
        if query == "!quit":
            break
        if query == "!history":
            print_history(session_id)
            continue

        # "지금까지 대화 보여줘" 또는 "뭐 물어봤" 명령어 처리
        if "대화 보여줘" in query or "뭐 물어봤" in query:
            handle_show_history_command(session_manager, session_id, query)
            continue

        session_manager.add_user_message(session_id, query)

        response = agent_executor.invoke({
            "query": query,
            "agent_scratchpad": session_manager.get_history(session_id)
        })

        pretty_print_response(query, response)

        if isinstance(response, dict) and "output" in response:
            session_manager.add_assistant_message(session_id, response["output"])
        else:
            session_manager.add_assistant_message(session_id, str(response))
