# 프로젝트 설명

이 프로젝트는 mem0 메모리 시스템과 crew AI MCP 툴을 이용한 멀티 에이전트 시스템을 활용한 예제 시스템입니다. 다양한 에이전트가 협력하여 복잡한 작업을 분담하고, 효율적으로 처리할 수 있도록 설계되었습니다.

1. Crew AI 기반 멀티에이전트
1. 동적 Crew 구성과 Task 플래닝
1. MCP 를 사용하는 에이전트
1. mem0를 이용한 에이전트 지식 자동 업데이트

# 실행 방법 (uv 기반)

1. 환경변수 설정
.env.example을 복사하여 .env 파일을 만든 후, API Key 를 설정

1. uv 로 빌드와 실행
```bash
uv run src/main.py
```

# 활용 예시: 
🤖 CrewAI Task Runner에 오신 것을 환영합니다!
달성하고자 하는 목표를 입력해주세요 (종료하려면 Ctrl+C 또는 Ctrl+D):
➡️  uengine.org 라는 회사를 위한 세무관련 제안서를 작성해.


# 영상
https://youtu.be/KLcQaINKAL0

# 적용 온라인 서비스 예시 (Process-GPT)
https://youtu.be/kd6_hKSQDYc?t=66


# 추가 명령어
   - 테스트 실행:
     ```bash
     uv python -m unittest
     ```
   - 기타 스크립트 실행도 `uv python [파일명.py]` 형식으로 실행하면 됩니다.
   - LLM 캐시 관리:
     ```bash
     # 모든 캐시 삭제
     uv python -m src.tools.cache_manager --clear
     
     # 48시간보다 오래된 캐시만 삭제
     uv python -m src.tools.cache_manager --clear --older-than 48
     ```

# 작업로그 영상

- part1: https://www.youtube.com/watch?v=aXJRFJQZV8s (agent 구성 설명 및 mem0 연동)
- part2: https://youtu.be/rAU5YCXLb2Q (mem0를 툴로 설정)
- part3: https://youtu.be/oxsLObGfTs0 (mcp 툴 설정)
- part4: https://youtu.be/mlwNocnyuS8

