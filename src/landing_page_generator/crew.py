from crewai import Agent, Crew, Process, Task
from langchain_community.agent_toolkits.file_management.toolkit import FileManagementToolkit
from tools.browser_tools import ScrapeWebsiteTool
from tools.file_tools import FileTools
from tools.search_tools import SearchInternetTool
from tools.template_tools import TemplateTools
# Import the official crewai-tools MCP integration and StdioServerParameters
from mcp import StdioServerParameters
from crewai_tools import MCPServerAdapter
from crewai.tools import BaseTool

import json
import ast
import os

from dotenv import load_dotenv
load_dotenv()


# Update MCP server configuration to use StdioServerParameters
mcp_server_params = StdioServerParameters(
    command="npx",
    args=["@playwright/mcp@latest"],
    env=os.environ
)

# Create MCP server adapter and get tools
mcp_server_adapter = MCPServerAdapter(mcp_server_params)
mcp_tools = mcp_server_adapter.tools

# Helper function to ensure all tools are BaseTool instances
def ensure_base_tools(tools_list):
    """Ensure all tools in the list are instances of BaseTool"""
    result = []
    for tool in tools_list:
        if isinstance(tool, BaseTool):
            result.append(tool)
    return result

class GenericCrew:
    """ExpandIdea crew"""
    def __init__(self):
        self.agents_config = self._load_config('config/agents.yaml')
        self.tasks_config = self._load_config('config/tasks.yaml')
        self.agents = []
        self.tasks = []
        self._setup_agents_and_tasks()
        
    def _load_config(self, path):
        # You'll need to implement config loading logic here
        # For now returning empty dict as placeholder
        return {}
        
    def _setup_agents_and_tasks(self):
        # Create agents
        self.senior_idea_analyst = self._create_senior_idea_analyst()
        self.senior_strategist = self._create_senior_strategist()
        self.agents = [self.senior_idea_analyst, self.senior_strategist]
        
        # Create tasks
        self.expand_idea_task = self._create_expand_idea_task()
        self.refine_idea_task = self._create_refine_idea_task()
        self.tasks = [self.expand_idea_task, self.refine_idea_task]

    def _create_senior_idea_analyst(self) -> Agent:
        search_tool = SearchInternetTool()
        scrape_tool = ScrapeWebsiteTool()
        tools = ensure_base_tools(mcp_tools)
        return Agent(
            config=self.agents_config['senior_idea_analyst'],
            allow_delegation=False,
            tools=tools,
            verbose=False,
            step_callback=lambda step_output: print(f"Step output: {step_output}")
        )
    
    def _create_senior_strategist(self) -> Agent:
        search_tool = SearchInternetTool()
        scrape_tool = ScrapeWebsiteTool()
        tools = ensure_base_tools(mcp_tools)
        return Agent(
            config=self.agents_config['senior_strategist'],
            allow_delegation=False,
            tools=tools,
            verbose=False,
            step_callback=lambda step_output: print(f"Step output: {step_output}")
        )
    
    def _create_expand_idea_task(self) -> Task:
        return Task(
            config=self.tasks_config['expand_idea_task'],
            agent=self.senior_idea_analyst,
        )
    
    def _create_refine_idea_task(self) -> Task:
        return Task(
            config=self.tasks_config['refine_idea_task'],
            agent=self.senior_strategist,
        )
    
    def get_crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

callback_handler = CallbackHandler()

class LandingPageCrew():
    def __init__(self, idea):
        self.idea = idea
    
    def run(self):
        try:
            expanded_idea = self.runExpandIdeaCrew(self.idea)
                
        finally:
            # Make sure to stop the MCP server adapter when done
            mcp_server_adapter.stop()
    
    def runExpandIdeaCrew(self, idea):
        inputs1 = {
            "idea": str(idea)
        }
        crew_instance = ExpandIdeaCrew()
        expanded_idea = crew_instance.get_crew().kickoff(inputs=inputs1)
        return str(expanded_idea)

  