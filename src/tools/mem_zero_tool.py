import os
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from mem0 import MemoryClient

class MemZeroToolSchema(BaseModel):
    agent_name: str = Field(..., description="에이전트 이름 (agent_id로 사용)")
    mode: str = Field(..., description="'add' 또는 'retrieve' 중 하나. add는 지식 축적, retrieve는 인출.")
    content: Optional[str] = Field(None, description="추가할 지식 내용 (mode=add일 때)")
    feedback: Optional[str] = Field(None, description="피드백 내용 (mode=add일 때 선택)")
    query: Optional[str] = Field(None, description="검색 쿼리 (mode=retrieve일 때)")

class MemZeroTool(BaseTool):
    name: str = "mem_zero_management"
    description: str = "에이전트별 지식 검색 툴. mode(add/retrieve)에 따라 지식 축적 또는 인출을 수행."
    args_schema: type = MemZeroToolSchema
    client: MemoryClient = Field(default=None, exclude=True)

    def __init__(self):
        super().__init__()
        self.client = MemoryClient(api_key=os.environ.get('MEM_ZERO_API_KEY'))

    def _run(self, agent_name: str, mode: str, content: Optional[str] = None, feedback: Optional[str] = None, query: Optional[str] = None):
        if mode == "add":
            if not content:
                return "content가 필요합니다."
            
            # Mem0 형식에 맞게 메시지 구성
            messages = [
                {"role": "user", "content": content}
            ]
            if feedback:
                messages.append({"role": "assistant", "content": feedback})
            
            # Mem0에 지식 추가
            self.client.add(messages, agent_id=agent_name)
            return f"새로운 지식이 {agent_name}에 추가되었습니다."
            
        elif mode == "retrieve":
            if not query:
                return "query가 필요합니다."
            
            # Mem0에서 지식 검색
            results = self.client.search(query, agent_id=agent_name)
            
            if not results:
                return "지식이 없습니다."
            
            # 검색 결과 포맷팅
            output = []
            for result in results:
                memory = result.get('memory', '')
                score = result.get('score', 0)
                output.append(f"[유사도: {score:.2f}]\n{memory}")
            
            return "\n\n---\n\n".join(output)
            
        else:
            return "mode는 add 또는 retrieve만 지원합니다." 