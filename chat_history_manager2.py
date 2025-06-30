########## chat_history_manager.py
"""
agent와 나눈 대화 내역을 저장하는 manager 파일입니다.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from langchain_community.chat_message_histories import SQLChatMessageHistory
import pymysql

load_dotenv()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASS = os.getenv("PASS")
DB = os.getenv("DB")

engine = create_engine(f"mysql+pymysql://{USER}:{PASS}@{HOST}:{PORT}/{DB}")
# engine = create_engine(f"mysql+pymysql://root:password@localhost:3306/{DB}")
conn = pymysql.connect(host=HOST,user=USER,password=PASS,db=DB,charset='utf8')

class ChatHistoryManager:
    def __init__(self):
        self.engine = engine
        self.store = {}  # ❗ optional cache
        self.curs = conn.cursor()
        
    def get_session_history(self, session_id: str) -> SQLChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = SQLChatMessageHistory(session_id=session_id, connection=self.engine)
        return self.store[session_id]
    
    def reset_session(self,session_id:str):
        query = f"delete from message_store where session_id = {session_id}"
        self.curs.execute(query)