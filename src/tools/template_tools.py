import json
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from crewai.tools import BaseTool


class LearnLandingPageOptionsSchema(BaseModel):
    input: Optional[str] = Field(None, description="Optional input parameter")


class CopyLandingPageTemplateSchema(BaseModel):
    landing_page_template: str = Field(..., description="The name of the landing page template to copy")


class LearnLandingPageOptionsTool(BaseTool):
    name: str = "Learn landing page options"
    description: str = "Learn the templates at your disposal"
    args_schema: type[BaseModel] = LearnLandingPageOptionsSchema
    
    def _run(self, input=None):
        templates = json.load(open("config/templates.json"))
        return json.dumps(templates, indent=2)
        
    async def _arun(self, input=None):
        return self._run(input)


class CopyLandingPageTemplateTool(BaseTool):
    name: str = "Copy landing page template to project folder"
    description: str = """Copy a landing page template to your project 
    folder so you can start modifying it, it expects 
    a landing page template folder as input"""
    args_schema: type[BaseModel] = CopyLandingPageTemplateSchema
    
    def _run(self, landing_page_template: str):
        source_path = Path(f"templates/{landing_page_template}")
        destination_path = Path(f"workdir/{landing_page_template}")
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_path, destination_path)
        return f"Template copied to {landing_page_template} and ready to be modified, main files should be under ./{landing_page_template}/src/components, you should focus on those."
        
    async def _arun(self, landing_page_template: str):
        return self._run(landing_page_template)


class TemplateTools:
    learn_landing_page_options = LearnLandingPageOptionsTool()
    copy_landing_page_template_to_project_folder = CopyLandingPageTemplateTool()
