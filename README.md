# 프로젝트 설명

이 프로젝트는 멀티 에이전트 시스템을 활용한 프로세스 자동화 및 관리 도구입니다. 다양한 에이전트가 협력하여 복잡한 작업을 분담하고, 효율적으로 처리할 수 있도록 설계되었습니다.

# 실행 방법 (uv 기반)

```bash
uv run python src/main.py
```

4. **추가 명령어**
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

# LLM 캐싱 시스템

이 프로젝트는 LLM(Large Language Model) 호출 결과를 캐싱하여 성능을 개선하고 API 비용을 절감하는 기능을 제공합니다.

## 주요 기능

1. **디스크 기반 캐싱**: LLM 응답을 디스크에 저장하여 동일한 요청에 대해 재사용할 수 있습니다.
2. **TTL(Time-To-Live) 관리**: 캐시 항목에 만료 시간을 설정하여 최신 정보를 유지합니다.
3. **LangChain 통합**: LangChain의 모델에서 캐싱을 자동으로 활용합니다.
4. **OpenAI Embedding 캐싱**: Embedding API 호출 결과를 캐싱하여 중복 호출을 방지합니다.

## 캐시 관리

캐시는 `.cache/llm` 디렉토리에 저장되며, 다음과 같은 방법으로 관리할 수 있습니다:

```python
# 코드에서 캐시 관리
from src.tools.cache_manager import CacheManager

# 모든 캐시 삭제
CacheManager.clear_cache()

# 24시간보다 오래된 캐시만 삭제
CacheManager.clear_cache(older_than_hours=24)
```

또는 커맨드 라인에서:

```bash
# 모든 캐시 삭제
python -m src.tools.cache_manager --clear

# 48시간보다 오래된 캐시만 삭제
python -m src.tools.cache_manager --clear --older-than 48
```

# TODO

1. task 간에 결과를 주고 받게

CrewAI에서 `{placeholder}` 값(예: `{idea}`)과 expected_output, 그리고 description의 연결 방식에 대해 설명드리겠습니다.

## 1. `{placeholder}` 값의 의미

CrewAI에서 description에 `{idea}`와 같은 placeholder를 사용하는 것은, 해당 Agent나 Task가 동적으로 입력받는 값을 설명에 삽입하기 위함입니다.  
예시:
```python
description="You are a creative agent. Your job is to generate a business plan for the following idea: {idea}"
```
여기서 `{idea}`는 실제 실행 시점에 값이 주입됩니다.

---

## 2. `{idea}` 값은 어디서 입력받아 주입되는가?

CrewAI의 Task나 Agent를 생성할 때, 보통 다음과 같이 `context` 또는 `input` 파라미터로 값을 전달합니다.

예시:
```python
from crewai import Task

task = Task(
    description="Generate a business plan for the following idea: {idea}",
    expected_output="A detailed business plan for {idea}",
    context={"idea": "AI-powered coffee shop"}
)
```
- 여기서 context에 `{"idea": "AI-powered coffee shop"}`를 전달하면, description과 expected_output의 `{idea}`가 해당 값으로 치환됩니다.

---

## 3. 어떤 방식으로 description을 작성하는가?

- description, expected_output 등에서 중괄호 `{}`로 감싼 이름을 placeholder로 사용합니다.
- 이 placeholder는 context나 input 등에서 전달된 값으로 자동 치환됩니다.
- 여러 개의 placeholder도 사용할 수 있습니다.

예시:
```python
description="Analyze the market for {product} in {region}"
context={"product": "electric scooters", "region": "Europe"}
```
실행 시:
```
Analyze the market for electric scooters in Europe
```

---

## 4. 실제 코드 예시

```python
from crewai import Task

task = Task(
    description="Write a summary about {topic}",
    expected_output="A concise summary of {topic}",
    context={"topic": "quantum computing"}
)
```
- 실행 시 description과 expected_output의 `{topic}`이 `"quantum computing"`으로 치환됩니다.

---

## 5. 요약

- description, expected_output 등에서 `{placeholder}`를 사용
- Task나 Agent 생성 시 context/input 등으로 값을 전달
- 실행 시점에 자동으로 치환됨

---

아주 좋은 질문입니다!  
첨부해주신 `tasks.yaml`을 보면, 각 Task의 description에서 `{idea}`, `{expanded_idea}`, `{file_content}` 등 다양한 placeholder를 사용하고 있지만,  
**output_key**나 명시적인 output 이름 선언 없이도 이전 단계의 값을 참조하고 있습니다.

### CrewAI에서 output_key 없이 값이 전달되는 원리

#### 1. **자동 컨텍스트 병합 및 추론**
CrewAI(및 유사한 오케스트레이션 프레임워크)는 일반적으로 **Task의 실행 결과를 자동으로 context에 병합**합니다.  
즉, 이전 Task의 output이 context 딕셔너리에 key-value 형태로 추가되고,  
이후 Task의 description에서 `{key}` 형태로 참조할 수 있습니다.

#### 2. **Key 추론 방식**
- **기본적으로는 Task의 이름이나 역할, 혹은 description에서 사용된 placeholder 이름을 기준으로 추론**합니다.
- 예를 들어, `expand_idea_task`의 output이 자동으로 `expanded_idea`라는 key로 context에 들어가고,  
  다음 Task에서 `{expanded_idea}`로 참조할 수 있습니다.
- 만약 명시적으로 output_key를 지정하지 않으면,  
  **Task 이름에서 `_task`를 제거한 snake_case 형태**(예: `expand_idea_task` → `expanded_idea`)로 key가 생성되는 경우가 많습니다.

#### 3. **실제 동작 예시**
- `expand_idea_task` → output이 `expanded_idea`로 context에 저장
- `component_content_task`에서 `{expanded_idea}`로 참조

#### 4. **CrewAI의 내부 동작(추정)**
- 각 Task 실행 후, 결과를 context에 저장
- 다음 Task 실행 시, context를 모두 합쳐서 placeholder를 치환
- 명시적 output_key가 없으면, Task 이름이나 description에서 유추

---

### 결론

- **output_key를 명시하지 않아도, CrewAI는 Task 이름이나 description에서 placeholder 이름을 추론하여 context에 값을 저장하고, 다음 Task에서 사용할 수 있게 해줍니다.**
- 이 덕분에 yaml에서 `{idea}`, `{expanded_idea}` 등으로 자연스럽게 값을 이어받아 사용할 수 있습니다.

---

#### 참고:  
CrewAI의 버전에 따라 동작 방식이 다를 수 있으니,  
정확한 동작은 실제 코드나 공식 문서를 참고하는 것이 가장 확실합니다.

---

**추가로 궁금한 점이나, 실제 코드에서 커스텀 output_key를 지정하는 방법이 궁금하다면 말씀해 주세요!**




1. Queue 기반 다중 실행 Thread 처리 & 프론트 스트림(watch) 처리
   - step_callback 혹은 listener 를 이용하여 처리결과를 supabase 의 특정 테이블에 쌓기 e.g. agent_log 에 각 thread id 를 두고 step 별로 쌓기 : threadId, task, output
   - 위의 output 들을 realtime 으로 보여주는 웹페이지
   - agent_thread이라는 요청 table을 계속 polling 하여 새로운  이라는 테이블에 요청이 들어오면 해당 건들을 polling loop를 돌면서 확인하여 status 가 queued 인 놈을 하나씩 처리 시작하면서 running  으로 설정한후 완료되면 done으로 설정. 
   - 기본적인 테스트는 table에 insert sql 로 요청사항 (goal, agent_names)을 입력하므로서 테스트 (이후에 프론트에서  이것에 insert 하고 그 상태를 watch 하므로서 진행상태 모니터링이 가능함. ) 키값은 thead_id로 잡고 agent_log 의 foreign key 로 잡혀서 해당 thread_id로 필터링 하면 세부 step 별 진행이 보이게.

2. 지식을 Tool 로 설정
   - 프로세스 인스턴스 정보 접근
   - 내부 문서들에 접근 (internal documents - memento / memento 서비스에 접근 에이젼트별 접근 권한 관리)
   - 본인(에이젼트)의 지식 접근
   - 피드백이 있고 배운게 있으면 본인의 지식에 적재

3. 