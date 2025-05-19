import yaml
import json
import os
from typing import Dict, List, Optional
from pathlib import Path
import openai
from crewai import Agent, Task, Crew, Process
from src.tools.search_tools import SearchInternetTool
from src.tools.file_tools import FileTools
from src.tools.browser_tools import ScrapeWebsiteTool
from mcp import StdioServerParameters
from crewai_tools import MCPServerAdapter
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from src.tools.mem_zero_tool import MemZeroTool
from mem0 import MemoryClient

class CrewConfigManager:
    def __init__(self, agents_config_path: str = "config/agents.yaml", mcp_config_path: str = "config/mcp.json", knol_task_path: str = "config/knol_task.yaml"):
        self.agents_config_path = agents_config_path
        self.mcp_config_path = mcp_config_path
        self.knol_task_path = knol_task_path
        self.agents_config = self._load_agents_config()
        self.mcp_tools = self._load_mcp_tools()
        #self.knol_task_config = self._load_knol_task_config()
        self.mem0_client = MemoryClient(api_key=os.environ.get('MEM_ZERO_API_KEY'))
        self.base_tools = {
            "search_internet": SearchInternetTool(),
            "write_file": FileTools.write_file,
            "scrape_website": ScrapeWebsiteTool(),
            #"knowledge_management": KnowledgeTool()
            "knowledge_management": MemZeroTool()
        }

    def _load_agents_config(self) -> Dict:
        """Load agents configuration from YAML file."""
        with open(self.agents_config_path, 'r') as f:
            return yaml.safe_load(f)

    def _load_mcp_tools(self) -> Dict[str, List]:
        """Load MCP tools using MCPServerAdapter, keeping tools separate by server."""
        try:
            with open(self.mcp_config_path, 'r') as f:
                mcp_config = json.load(f)
                tools = {}
                
                # Get MCP tools for each server separately
                for server_name, server_config in mcp_config.get("mcpServers", {}).items():
                    mcp_server_params = StdioServerParameters(
                        command=server_config.get("command", "npx"),
                        args=server_config.get("args", ["@playwright/mcp@latest"]),
                        env=os.environ  # 필요시 server_config에서 env를 받아올 수도 있음
                    )
                    mcp_server_adapter = MCPServerAdapter(mcp_server_params)
                    tools[server_name] = mcp_server_adapter.tools
                    
                return tools
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Warning: Could not load MCP config from {self.mcp_config_path}")
            return {}

    def _load_knol_task_config(self) -> Dict:
        """Load knowledge task configuration from YAML file."""
        try:
            with open(self.knol_task_path, 'r') as f:
                return yaml.safe_load(f)
        except (FileNotFoundError, yaml.YAMLError):
            print(f"Warning: Could not load knowledge task config from {self.knol_task_path}")
            return {}

    def _get_tools_for_agent(self, agent_config: Dict) -> List:
        """Get tools list for an agent based on their configuration."""
        tools = []
        if "tools" in agent_config:
            tool_names = [t.strip() for t in agent_config["tools"].split(",")]
            
            for tool_name in tool_names:
                if tool_name in self.base_tools:
                    tools.append(self.base_tools[tool_name])
                elif tool_name.endswith("(mcp)"):
                    # Extract the actual tool name without (mcp)
                    mcp_server_name = tool_name[:-5]  # Remove (mcp)
                    if mcp_server_name in self.mcp_tools:
                        # Add all tools from the specified MCP server
                        tools.extend(self.mcp_tools[mcp_server_name])
        # knowledge_management 툴은 항상 추가 [off]
        tools.append(self.base_tools["knowledge_management"])
        return tools

    def create_crew(self, topic: str) -> Crew:
        """Create a Crew instance based on the topic using CrewAI's built-in planning."""
        # Create agents from configuration
        agents = []
        for agent_name, agent_config in self.agents_config.items():
            # Get tools for this agent
            tools = self._get_tools_for_agent(agent_config)
            
            # Create agent
            agent = Agent(
                role=agent_name,
                goal=agent_config["goal"],
                backstory=agent_config["backstory"],
                allow_delegation=True,
                tools=tools,
                **{k: v for k, v in agent_config.items() 
                   if k not in ["role", "goal", "backstory", "tools"]}
            )
            agents.append(agent)

        # Create initial task
        initial_task = Task(
            description=f"주어진 목표를 달성하기 위한 계획을 수립하고 실행하세요: {topic}",
            agent=agents[0],  # First agent will be the initial planner
            expected_output="목표 달성을 위한 상세 실행 계획과 각 에이전트의 역할이 포함된 문서"
        )

        # Create LLM for the manager
        llm = ChatOpenAI(
            model="gpt-4.1",
            temperature=0.7
        )

        # Create and return the crew with hierarchical planning
        return Crew(
            agents=agents,
            tasks=[initial_task],
            manager_llm=llm,
            process=Process.hierarchical,
            verbose=True,
            planning=True
        )

    def _create_prompt(self, topic: str) -> str:
        """Create the prompt for OpenAI with available agents."""
        agent_names = list(self.agents_config.keys())
        
        prompt = f"""You are a tool for creating configurations for an Agent framework called CrewAI.

        To achieve a certain Goal, multiple Agents will collaborate to solve problems. Therefore, divide the necessary expertise areas to solve the problem with at least two or more Agent if possible.
        It mainly consists of the configuration of Agents and the Tasks each Agent performs. And divide the Tasks so that each Agent can deal with problems in their expertise area by passing work among themselves.
        Since the Tasks will be executed sequentially, they must be defined in order.
        the result MUST be written in Korean language.
        All results must be generated in JSON format with key values(as valid JSON using double quotes around keys and values).

        we have following agents: {agent_names}

        The resulting json will be as follows (Please use VALID JSON with double-quoted for key and value):
        {{
            "agents":[{{
                "name": "name of the agent (one of the listed agent)",
                "goal": "goal of the agent (optional, will use default if not provided)"
            }}],
            "tasks":[
                {{
                "description": "Task description in Korean",
                "agent": "agent assigned to the task (e.g., agent)",
                "expected_output": "expected output of the task"
                }}
            ]
        }}

        Please configure a crew for the following mission: {topic}
        """
        return prompt 