import os
import json
import base64
import asyncio
from typing import Optional, Dict, Any, Type
from dotenv import load_dotenv

from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field

import mcp
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 환경 변수 로드
load_dotenv()

class NaverSearchInput(BaseModel):
    """네이버 검색 입력 스키마"""
    query: str = Field(description="검색어")
    display: Optional[int] = Field(default=10, description="한 번에 가져올 결과 수")
    start: Optional[int] = Field(default=1, description="검색 시작 위치")
    sort: Optional[str] = Field(default="sim", description="정렬 방식 (sim: 유사도순, date: 날짜순)")

class NaverSearchTool(BaseTool):
    """네이버 검색 MCP 도구"""
    name: str = "naver_search"
    description: str = """
    네이버 웹문서 검색을 수행하는 도구입니다.
    한국어 검색에 특화되어 있으며, 최신 정보를 찾을 때 유용합니다.
    """
    args_schema: Type[BaseModel] = NaverSearchInput
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # MCP 서버 파라미터를 private 속성으로 설정
        object.__setattr__(self, '_server_params', self._create_server_params())
    
    def _create_server_params(self) -> StdioServerParameters:
        """MCP 서버 파라미터 생성"""
        return StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@smithery/cli@latest",
                "run",
                "@isnow890/naver-search-mcp",
                "--key",
                os.getenv("SMITHERY_API_KEY", "9a537df8-5657-4fbc-9d7f-3e00f777fddb"),
                "--config",
                self._get_config_b64()
            ]
        )
    
    @property
    def server_params(self) -> StdioServerParameters:
        """서버 파라미터 접근"""
        return self._server_params
    
    def _get_config_b64(self) -> str:
        """네이버 API 설정을 base64로 인코딩"""
        config = {
            "NAVER_CLIENT_ID": os.getenv("NAVER_CLIENT_ID"),
            "NAVER_CLIENT_SECRET": os.getenv("NAVER_CLIENT_SECRET")
        }
        return base64.b64encode(json.dumps(config).encode()).decode()
    
    def _run(self, query: str, display: int = 10, start: int = 1, sort: str = "sim") -> str:
        """동기 실행 (비동기 함수를 래핑)"""
        return asyncio.run(self._arun(query, display, start, sort))
    
    async def _arun(self, query: str, display: int = 10, start: int = 1, sort: str = "sim") -> str:
        """비동기 네이버 검색 실행"""
        try:
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # MCP 서버 초기화
                    await session.initialize()
                    
                    # 검색 실행
                    result = await session.call_tool(
                        "search_webkr",
                        {
                            "query": query,
                            "display": display,
                            "start": start,
                            "sort": sort
                        }
                    )
                    
                    # 결과 포맷팅
                    if result.content:
                        search_results = []
                        for item in result.content:
                            if hasattr(item, 'text'):
                                data = json.loads(item.text)
                                for article in data.get('items', []):
                                    search_results.append({
                                        'title': article.get('title', '').replace('<b>', '').replace('</b>', ''),
                                        'description': article.get('description', '').replace('<b>', '').replace('</b>', ''),
                                        'link': article.get('link', ''),
                                        'pubDate': article.get('pubDate', '')
                                    })
                        
                        return json.dumps(search_results, ensure_ascii=False, indent=2)
                    else:
                        return "검색 결과를 찾을 수 없습니다."
                        
        except Exception as e:
            return f"검색 중 오류가 발생했습니다: {str(e)}"

class NaverSearchAgent:
    """네이버 검색 기능을 가진 ChatOpenAI 에이전트"""
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # 네이버 검색 도구 초기화
        self.naver_tool = NaverSearchTool()
        
        # LLM에 도구 바인딩
        self.llm_with_tools = self.llm.bind_tools([self.naver_tool])
    
    async def search_and_answer(self, question: str) -> str:
        """질문에 대해 네이버 검색을 수행하고 답변 생성"""
        
        # 1단계: 검색이 필요한지 판단하고 검색 수행
        search_prompt = f"""
        다음 질문에 답하기 위해 네이버 검색을 수행해주세요:
        질문: {question}
        
        적절한 검색어를 사용하여 naver_search 도구를 호출해주세요.
        """
        
        # 검색 수행
        search_response = await self.llm_with_tools.ainvoke([HumanMessage(content=search_prompt)])
        
        # 도구 호출이 있다면 실행
        search_results = ""
        if search_response.tool_calls:
            for tool_call in search_response.tool_calls:
                if tool_call["name"] == "naver_search":
                    search_results = await self.naver_tool._arun(**tool_call["args"])
        
        # 2단계: 검색 결과를 바탕으로 최종 답변 생성
        if search_results:
            final_prompt = f"""
            질문: {question}
            
            네이버 검색 결과:
            {search_results}
            
            위 검색 결과를 바탕으로 질문에 대한 정확하고 도움이 되는 답변을 작성해주세요.
            검색 결과에서 중요한 정보를 추출하여 자연스럽게 답변을 구성해주세요.
            """
            
            final_response = await self.llm.ainvoke([HumanMessage(content=final_prompt)])
            return final_response.content
        else:
            return "죄송합니다. 검색 결과를 가져올 수 없어서 질문에 답변드리기 어렵습니다."
    
    def search_and_answer_sync(self, question: str) -> str:
        """동기 버전의 검색 및 답변"""
        return asyncio.run(self.search_and_answer(question))

# 사용 예제
async def main():
    """메인 실행 함수"""
    
    # 에이전트 초기화
    agent = NaverSearchAgent()
    
    # 테스트 질문들
    questions = [
        "2024년 한국 경제 성장률은 어떻게 되나요?",
        "최근 K-pop 트렌드는 무엇인가요?",
        "서울 맛집 추천해주세요"
    ]
    
    for question in questions:
        print(f"\n질문: {question}")
        print("=" * 50)
        
        try:
            answer = await agent.search_and_answer(question)
            print(f"답변: {answer}")
        except Exception as e:
            print(f"오류: {e}")
        
        print("\n" + "="*50)

# 동기 버전 사용 예제
def sync_example():
    """동기 방식 사용 예제"""
    agent = NaverSearchAgent()
    
    question = "최신 AI 기술 동향은?"
    answer = agent.search_and_answer_sync(question)
    print(f"질문: {question}")
    print(f"답변: {answer}")

if __name__ == "__main__":
    # 비동기 실행
    # asyncio.run(main())
    
    # 또는 동기 실행
    sync_example()