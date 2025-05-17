import os
import sys
from src.tools.knowledge_tool import KnowledgeTool

# OpenAI API 키 확인
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    api_key = input("OpenAI API 키를 입력하세요: ")
    os.environ["OPENAI_API_KEY"] = api_key

def test_knowledge_tool():
    print(f"API 키: {os.environ['OPENAI_API_KEY'][:5]}...{os.environ['OPENAI_API_KEY'][-4:]}")
    
    # 지식 관리 도구 초기화
    tool = KnowledgeTool()
    
    # 테스트 에이전트 이름
    agent_name = "test_agent"
    
    # 1. 지식 추가 테스트
    content = "ChromaDB는 벡터 데이터베이스로, 임베딩 기반 검색을 효율적으로 수행할 수 있습니다."
    feedback = "이 정보는 매우 유용합니다."
    
    print("===== 지식 추가 테스트 =====")
    add_result = tool._run(
        agent_name=agent_name, 
        mode="add", 
        content=content, 
        feedback=feedback
    )
    print(add_result)
    
    # 2. 지식 검색 테스트
    query = "벡터 데이터베이스"
    
    print("\n===== 지식 검색 테스트 =====")
    retrieve_result = tool._run(
        agent_name=agent_name, 
        mode="retrieve", 
        query=query
    )
    print(retrieve_result)

if __name__ == "__main__":
    test_knowledge_tool() 