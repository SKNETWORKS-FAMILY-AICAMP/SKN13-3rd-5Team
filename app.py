# app.py
import os
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from typing import TypedDict, Optional

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import *
from langchain_core.messages import HumanMessage, AIMessage

from langgraph.graph import StateGraph, END

from llm_tools.chat_history_manager2 import ChatHistoryManager

from llm_tools.retriever import RAG_tool
from llm_tools.get_weather import get_weather_by_location_and_date
from llm_tools.google_places import get_places_by_keyword_and_location
from llm_tools.naver_search import NaverSearchTool

# ✅ 환경설정
load_dotenv()
cur_date = datetime.now()

# ✅ 메시지 관리자 및 도구 설정
message_manager = ChatHistoryManager()
tools = [RAG_tool, get_weather_by_location_and_date, get_places_by_keyword_and_location]

# ✅ 프롬프트 구성
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", f"""
당신은 문화유산 데이트코스 생성 모델입니다.
현재 날짜는 {cur_date}입니다.

[Guidelines]
1. 대한민국의 문화유산에 대한 정보는 RAG_tool 도구를 사용하세요.
2. 날씨 정보는 get_weather_by_location_and_date 도구를 사용하세요.
3. 식당, 명소 등 실제 장소 검색은 get_places_by_keyword_and_location 도구를 사용하세요.

정확한 정보를 바탕으로 데이트 코스를 추천하세요.
"""),
    MessagesPlaceholder(variable_name="history", optional=True),
    ("human", "{query}"),
    MessagesPlaceholder(variable_name="agent_scratchpad", optional=True)
])

# ✅ Agent 구성
agent = create_tool_calling_agent(
    llm=ChatOpenAI(model_name="gpt-4.1"),
    tools=tools,
    prompt=agent_prompt
)

agent_executor2 = AgentExecutor(agent=agent, tools=tools)

agent_executor = RunnableWithMessageHistory(
    runnable=agent_executor2,
    get_session_history=message_manager.get_session_history,
    input_messages_key="query",
    history_messages_key="history"
)

# ✅ LangGraph 상태 정의
class GraphState(TypedDict):
    query: str
    session_id: str
    response: Optional[str]

# ✅ 노드 정의
def parse_node(state: GraphState) -> GraphState:
    return {"query": state["query"]}

def agent_node(state: GraphState) -> GraphState:
    result = agent_executor.invoke(
        {"query": state["query"]},
        config={"configurable": {"session_id": state["session_id"]}}
    )
    return {
        "query": state["query"],
        "session_id": state["session_id"],
        "response": result["output"]
    }

def respond_node(state: GraphState) -> GraphState:
    return {
        "query": state["query"],
        "session_id": state.get("session_id", "NULL")
    }

# ✅ LangGraph 구성
graph = StateGraph(GraphState)
graph.add_node("parse", parse_node)
graph.add_node("run_agent", agent_node)
graph.add_node("respond", respond_node)

graph.set_entry_point("parse")
graph.add_edge("parse", "run_agent")
graph.add_edge("run_agent", "respond")
graph.add_edge("respond", END)

app = graph.compile()

# ✅ Streamlit UI
st.set_page_config(page_title="여행나래", page_icon="🏛️")
st.title("🏛️ 여행나래")

# 🆔 세션 ID 입력
session_id = st.text_input("🆔 ID를 입력하세요", value="우삣삐", disabled=False)

# 🔄 히스토리 초기화 버튼
if st.button("♻️ 대화 초기화"):
    message_manager.reset_session(session_id)
    st.rerun()  # 새로고침으로 히스토리 즉시 반영

# ✅ DB 히스토리 불러와서 채팅 말풍선으로 출력
history = message_manager.get_session_history(session_id)
for msg in history.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# 💬 사용자 질문 입력 (엔터 입력 지원)
query = st.chat_input("질문을 입력하세요 (예: '내일 경주 데이트코스 추천해줘')")

if query:
    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(query)

    # 챗봇 응답 출력
    with st.chat_message("assistant"):
        with st.spinner("AI가 답변을 생성 중입니다..."):
            result = app.invoke({"query": query, "session_id": session_id})
            response = result.get("response", "응답이 없습니다.")
            st.markdown(response)