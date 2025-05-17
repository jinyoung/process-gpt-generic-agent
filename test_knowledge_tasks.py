#!/usr/bin/env python3

import os
import yaml
from src.crew_config_manager import CrewConfigManager

def test_knowledge_tasks():
    """테스트: 에이전트별 지식 관리 태스크가 올바르게 추가되는지 확인"""
    
    # CrewConfigManager 초기화
    manager = CrewConfigManager(
        agents_config_path="config/agents.yaml",
        mcp_config_path="config/mcp.json",
        knol_task_path="config/knol_task.yaml"
    )
    
    # Crew 생성
    test_goal = "테스트 목표: 웹사이트 개선"
    crew = manager.create_crew(test_goal)
    
    # 결과 확인
    agent_names = [agent.role for agent in crew.agents]
    print(f"\n에이전트 목록 ({len(agent_names)}개): {', '.join(agent_names)}")
    
    # 각 에이전트별 태스크 확인
    tasks_by_agent = {}
    for task in crew.tasks:
        agent_name = task.agent.role
        if agent_name not in tasks_by_agent:
            tasks_by_agent[agent_name] = []
        tasks_by_agent[agent_name].append(task.description[:50] + "..." if len(task.description) > 50 else task.description)
    
    # 지식 관리 태스크가 추가되었는지 확인
    knol_config = None
    with open("config/knol_task.yaml", 'r') as f:
        knol_config = yaml.safe_load(f)["task_config"]
    
    print("\n== 에이전트별 태스크 목록 ==")
    for agent_name, tasks in tasks_by_agent.items():
        print(f"\n[{agent_name}] - {len(tasks)}개 태스크:")
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. {task}")
        
        # 마지막 태스크가 지식 관리 태스크인지 확인
        expected_prefix = knol_config["description"].format(agent_name=agent_name)[:30]
        actual_last_task = tasks[-1][:30]
        
        if expected_prefix in actual_last_task:
            print(f"  ✅ 지식 관리 태스크 확인됨")
        else:
            print(f"  ❌ 지식 관리 태스크 누락됨!")
            print(f"     - 기대: {expected_prefix}...")
            print(f"     - 실제: {actual_last_task}...")
    
    print("\n✅ 테스트 완료!")

if __name__ == "__main__":
    test_knowledge_tasks() 