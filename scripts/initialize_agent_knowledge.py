from typing import List, Dict
from mem0 import MemoryClient
import os
from dotenv import load_dotenv


def initialize_agent_knowledge():
    load_dotenv()
    
    client = MemoryClient(api_key=os.environ.get('MEM_ZERO_API_KEY'))  # Initialize memory client (Cloud API mode)
    
    # # Knowledge initialization for Senior Idea Analyst
    # idea_analyst_knowledge = [
    #     {"role": "user", "content": "What makes a great product idea?"},
    #     {"role": "assistant", "content": "A great product idea solves a real pain point, has a clear target market, and offers unique value. It should be feasible to implement and have potential for growth."}
    # ]
    # client.add(idea_analyst_knowledge, agent_id="senior_idea_analyst")

    # # Knowledge initialization for Senior Communications Strategist
    # strategist_knowledge = [
    #     {"role": "user", "content": "Explain the Golden Circle method."},
    #     {"role": "assistant", "content": "The Golden Circle by Simon Sinek focuses on WHY (purpose), HOW (process), and WHAT (product). Starting with 'why' creates emotional connections and inspires action."}
    # ]
    # client.add(strategist_knowledge, agent_id="senior_strategist")

    # # Knowledge initialization for Senior React Engineer
    # react_engineer_knowledge = [
    #     {"role": "user", "content": "What are the key elements of a high-converting landing page?"},
    #     {"role": "assistant", "content": "A high-converting landing page needs clear value proposition, intuitive navigation, mobile responsiveness, fast loading times, and strategic CTAs. Using Tailwind CSS for styling ensures consistent, beautiful design."}
    # ]
    # client.add(react_engineer_knowledge, agent_id="senior_react_engineer")

    # # Knowledge initialization for Senior Content Editor
    # content_editor_knowledge = [
    #     {"role": "user", "content": "What makes website content engaging?"},
    #     {"role": "assistant", "content": "Engaging content is clear, concise, and value-driven. It uses active voice, maintains consistent tone, includes compelling headlines, and focuses on benefits rather than features."}
    # ]
    # client.add(content_editor_knowledge, agent_id="senior_content_editor")

    # # Knowledge initialization for Senior Tax Accountant (세무사)
    # tax_accountant_knowledge = [
    #     {"role": "user", "content": "법인세 감면 혜택에 대해 설명해주세요."},
    #     {"role": "assistant", "content": """
    #     법인세 감면 혜택의 주요 내용은 다음과 같습니다:
    #     1. 신생 법인 감면: 설립 3년 이내 법인은 기본세율에서 10% 감면
    #     2. 여성 대표 감면: 대표이사가 여성인 경우 5% 추가 감면
    #     3. 지역 감면: 비수도권 소재 기업은 지방세 3% 추가 감면
    #     4. 소규모 신생 기업: 연매출 1억원 이하 & 설립 1년 미만은 전액 면제
        
    #     중요 규정:
    #     - 기본 법인세율: 20%
    #     - 최대 감면율: 20% (중복 적용 가능하나 상한선 존재)
    #     - 업종별 제한: 제조업은 지방세 감면 제외, IT 서비스업은 여성 대표 + 지방 감면 동시 적용 가능
    #     """}
    # ]
    # client.add(tax_accountant_knowledge, agent_id="senior_tax_accountant")

    # Knowledge initialization for Senior Proposal Expert (제안서 전문가)
    proposal_expert_knowledge = [
        {"role": "user", "content": "제안서 작성 시 고려해야 할 주요 사항은 무엇인가요?"},
        {"role": "assistant", "content": """
        제안서 작성 시 고려사항:
        
        1. 문서 형식 요구사항:
        - 공공기관: HWP 또는 정부 양식 필수
        - 민간기업: PPT 선호 (일부 PDF 문서형 요구)
        - 상장기업: IR 가치 제안 항목 필수 포함
        
        2. 평가 유형별 중점 사항:
        - 기술 중심: 아키텍처 다이어그램, 기능 명세 강조
        - 가격 중심: 비용 상세 내역, 유지보수 조건 강조
        - 성과 중심: 유사 사례, 성공사례 강조
        
        3. 특수 요구사항:
        - 보안 민감 기업: 데이터 보안 항목, 서버 위치 명시 필수
        - 검토 프로세스: 일반 기업 최소 1회, 공공기관 최소 2회 내부 검토 필수
        """}
    ]
    client.add(proposal_expert_knowledge, agent_id="senior_proposal_expert")

if __name__ == "__main__":
    initialize_agent_knowledge() 