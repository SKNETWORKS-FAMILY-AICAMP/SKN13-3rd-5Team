########## chat_history_manager.py
"""
agent와 나눈 대화 내역을 저장하는 manager 파일입니다.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from langchain_community.chat_message_histories import SQLChatMessageHistory

load_dotenv()
HOST = "127.0.0.1"
PORT = "3306"
USER = "root"
PASS = "1111"
DB = "project3"

engine = create_engine(f"mysql+pymysql://{USER}:{PASS}@{HOST}:{PORT}/{DB}")

class ChatHistoryManager:
    def __init__(self):
        self.engine = engine
        self.store = {}  # ❗ optional cache

    def get_session_history(self, session_id: str) -> SQLChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = SQLChatMessageHistory(session_id=session_id, connection=self.engine)
        return self.store[session_id]