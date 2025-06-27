# app.py
import os
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import *
from llm_tools.retriever import RAG_tool
from llm_tools.get_weather import get_weather_by_location_and_date
from chat_history_manager import ChatHistoryManager

# 환경변수 로딩
load_dotenv()
cur_date = datetime.now()

# 챗봇 설정
message_manager = ChatHistoryManager()
tools = [RAG_tool, get_weather_by_location_and_date]

agent_prompt = ChatPromptTemplate.from_messages([
    ("system", f"""
당신은 문화 유산 탐사대입니다.
현재 날짜는 {cur_date}입니다.

[Guidelines]
1. 대한민국의 문화유산에 대한 정보는 RAG_tool 도구를 사용하세요.
2. 날씨 정보는 get_weather_by_location_and_date 도구를 사용하세요.

각 도구의 목적과 기능을 정확하게 이해하고 적절한 상황에서 사용하세요.
"""),
    MessagesPlaceholder(variable_name="history", optional=True),
    ("human", "{query}"),
    MessagesPlaceholder(variable_name="agent_scratchpad", optional=True)
])

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

# LangGraph 상태 정의
class GraphState(TypedDict):
    query: str
    session_id: str
    response: Optional[str]

# 노드 정의
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

# LangGraph 구성
graph = StateGraph(GraphState)
graph.add_node("parse", parse_node)
graph.add_node("run_agent", agent_node)
graph.add_node("respond", respond_node)

graph.set_entry_point("parse")
graph.add_edge("parse", "run_agent")
graph.add_edge("run_agent", "respond")
graph.add_edge("respond", END)

app = graph.compile()

# Streamlit UI
st.set_page_config(page_title="여행나래", page_icon="🏛️")
st.title("🏛️여행나래")

# 세션 ID 입력
session_id = st.text_input("🆔ID를 입력하세요", value="user1")

# 질문 입력 (엔터 입력 시 바로 실행됨)
query = st.text_input("💬 궁금한 점을 입력하세요 (예: '내일 경복궁 갈건데 데이트 코스 짜줘.')", key="query_input")


if st.button("질문하기") and query.strip():
    with st.spinner("AI가 답변을 생성 중입니다..."):
        result = app.invoke({"query": query, "session_id": session_id})
        st.markdown("### 📌 답변")
        st.success(result.get("response", "응답이 없습니다."))
        