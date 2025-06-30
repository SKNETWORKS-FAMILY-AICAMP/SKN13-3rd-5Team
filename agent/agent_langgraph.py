# ✅ LangGraph 기반으로 리팩토링된 agent.py

import os
from datetime import datetime
from dotenv import load_dotenv
from typing import TypedDict, Optional

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langgraph.graph import StateGraph, END
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import *

from llm_tools.chat_history_manager import ChatHistoryManager

from llm_tools.retriever import RAG_tool
from llm_tools.get_weather import get_weather_by_location_and_date
from llm_tools.google_places import get_places_by_keyword_and_location
from llm_tools.naver_search import NaverSearchTool

load_dotenv()

message_manager = ChatHistoryManager()
naver_search = NaverSearchTool()

# ✅ 1. Agent 및 Tool 설정 (기존과 동일)
cur_date = datetime.now()

tools = [RAG_tool,get_weather_by_location_and_date,get_places_by_keyword_and_location]
# tools = [RAG_tool,get_weather_by_location_and_date,naver_search]

agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", f"""
당신은 문화 유산 탐사대입니다.
현재 날짜는 {cur_date}입니다.

[Guidelines]
1. 대한민국의 문화유산에 대한 정보는 RAG_tool 도구를 사용하세요.
2. 날씨 정보는 get_weather_by_location_and_date 도구를 사용하세요.
3. 실제 식당, 카페, 명소를 찾을 때는 naver_search 도구를 사용하세요.

최대한 정확한 정보를 제공하고, 도구를 조합해서 사용자 요청을 충실히 수행하세요.
**없는 장소를 만들어 내지 마시오.**

각 도구의 목적과 기능을 정확하게 이해하고 각 적절한 상황에서 사용하세요.
각 도구들을 결합해서 사용자의 요청에 정확한 대답을 하세요.
항상 가장 최신의 정확한 정보를 제공하기 위해 노력하세요.
"""),
        MessagesPlaceholder(variable_name="history", optional=True),
        ("human", "{query}"),
        MessagesPlaceholder(variable_name="agent_scratchpad", optional=True)
    ]
)

agent = create_tool_calling_agent(
    llm=ChatOpenAI(model_name="gpt-4.1"),
    tools=tools,
    prompt=agent_prompt
)

agent_executor2 = AgentExecutor(agent=agent,tools=tools)

agent_executor = RunnableWithMessageHistory(
    runnable=agent_executor2,
    get_session_history=message_manager.get_session_history,
    input_messages_key="query",
    history_messages_key="history"
)

# ✅ 2. LangGraph용 상태 정의
class GraphState(TypedDict):
    query: str
    session_id: str
    response: Optional[str]

# ✅ 3. 노드 정의 (각 단계를 함수로 분리)
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
        "response": result["output"]}

def respond_node(state: GraphState) -> GraphState:
    print(f"\n🧠 응답: {state['response']}")
    return {
        "query": state["query"],
        "session_id": state.get("session_id", "NULL")  # 기본값 "user1"
    }

# ✅ 4. LangGraph 그래프 구성
graph = StateGraph(GraphState)
graph.add_node("parse", parse_node)
graph.add_node("run_agent", agent_node)
graph.add_node("respond", respond_node)

graph.set_entry_point("parse")
graph.add_edge("parse", "run_agent")
graph.add_edge("run_agent", "respond")
graph.add_edge("respond", END)

app = graph.compile()


session_id = input("\n >>> id를 입력하세요: ").strip()
print(f"🗂️  세션 '{session_id}' 으로 저장됩니다.")

# ✅ 5. 실행 루프 (간단한 입력 반복)
while True:
    query = input("\n\n >>> 쿼리를 입력하세요: ")
    if query == "!quit":
        break
    app.invoke({"query": query, "session_id": session_id})
