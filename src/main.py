#!/usr/bin/env python3

import os
from crew_config_manager import CrewConfigManager
from dotenv import load_dotenv
import json

def main():
    # Load environment variables from .env file
    load_dotenv()

    # 설정 파일 경로
    agents_config = 'config/agents.yaml'
    mcp_config = 'config/mcp.json'

    try:
        print("\n🤖 CrewAI Task Runner에 오신 것을 환영합니다!")
        print("달성하고자 하는 목표를 입력해주세요 (종료하려면 Ctrl+C 또는 Ctrl+D):")
        print("➡️  ", end='', flush=True)
        
        goal = input().strip()
        
        if not goal:
            print("\n⚠️  목표가 입력되지 않았습니다. 기본 목표로 진행합니다: www.uengine.org의 개선안 도출")
            goal = "www.uengine.org의 개선안 도출"

        # Initialize CrewConfigManager
        manager = CrewConfigManager(
            agents_config_path=agents_config,
            mcp_config_path=mcp_config
        )

        # Crew 구성 정보 JSON 출력
        crew_config = manager.generate_crew_config(goal)
        print("\n🧑‍💻 AI 크루 구성 결과 (JSON):")
        print(json.dumps(crew_config, ensure_ascii=False, indent=2))

        # Create and run the crew
        print(f"\n🎯 입력된 목표: {goal}")
        print("\n🤖 AI 크루를 구성하고 작업을 시작합니다...\n")
        
        crew = manager.create_crew(goal)
        result = crew.kickoff()
        
        print("\n✨ 작업 결과:")
        print(result)

    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 프로그램을 종료합니다.")
        return 0
    except Exception as e:
        import traceback
        print(f"\n❌ 오류가 발생했습니다: {str(e)}")
        print(traceback.format_exc())
        return 1

    return 0

if __name__ == "__main__":
    exit(main()) 