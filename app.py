# app.py

import streamlit as st
from datetime import datetime
from agent_langgraph import app as langgraph_app  # agent.py에서 graph.compile()로 생성된 app 객체 임포트
from chat_history_manager import ChatHistoryManager

# 세션 상태 초기화
if "session_id" not in st.session_state:
    st.session_state["session_id"] = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.set_page_config(page_title="문화유산 탐사대 챗봇", page_icon="🗺️", layout="wide")

st.title("🗺️ 문화유산 탐사대 챗봇")
st.markdown("""
- 대한민국 문화유산, 날씨, 명소, 식당 등 정보를 물어보세요.
- `!quit` 입력 시 대화 종료.
""")

# 세션 ID 입력
with st.sidebar:
    st.header("세션 관리")
    session_id = st.text_input("세션 ID", value=st.session_state["session_id"])
    if st.button("세션 변경"):
        st.session_state["session_id"] = session_id
        st.session_state["chat_history"] = []
        st.success(f"세션이 '{session_id}'로 변경되었습니다.")

# 채팅 입력 폼
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("질문을 입력하세요:", key="user_input")
    submitted = st.form_submit_button("전송")

# 대화 기록 표시
st.markdown("### 💬 대화 기록")
for chat in st.session_state["chat_history"]:
    st.markdown(f"**사용자:** {chat['user']}")
    st.markdown(f"> {chat['query']}")
    st.markdown(f"**탐사대:** {chat['response']}")
    st.markdown("---")

# 입력 처리 및 LangGraph 실행
if submitted and user_input:
    if user_input.strip() == "!quit":
        st.info("대화를 종료합니다. 새로고침(F5)으로 재시작하세요.")
        st.stop()

    # LangGraph 실행
    with st.spinner("탐사대가 답변을 준비 중입니다..."):
        result = langgraph_app.invoke({
            "query": user_input,
            "session_id": st.session_state["session_id"]
        })
        response = result.get("response", "답변을 생성하지 못했습니다.")

    # 대화 기록 저장
    st.session_state["chat_history"].append({
        "user": st.session_state["session_id"],
        "query": user_input,
        "response": response
    })

    # 바로 최신 대화 표시
    st.experimental_rerun()

# 대화 기록 초기화 버튼
if st.button("대화 기록 초기화"):
    st.session_state["chat_history"] = []
    st.success("대화 기록이 초기화되었습니다.")

