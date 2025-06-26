# chat_history_manager.py

from langchain_core.chat_history import InMemoryChatMessageHistory

class ChatHistoryManager:
    def __init__(self):
        self.history = InMemoryChatMessageHistory()

    def add_user_message(self, text):
        self.history.add_user_message(text)

    def add_assistant_message(self, text):
        self.history.add_ai_message(text)

    def get_history(self):
        """
        현재까지의 대화 메시지 리스트 반환 (LangChain Message 객체 리스트)
        """
        return self.history.messages

    def clear_history(self):
        self.history.clear()
