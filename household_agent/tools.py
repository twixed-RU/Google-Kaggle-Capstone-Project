from .sub_agents.google_search_agent import google_search_agent
from google.adk.tools import AgentTool
from .sub_agents.maintenance_analyzer_agent import maintenance_analyzer_agent

google_search_tool = AgentTool(google_search_agent)
maintenance_analyzer_tool = AgentTool(maintenance_analyzer_agent)

def get_zip_code_tool() -> str:
    # In a real implementation, this would return a tool that provides the zip code.
    return "22015"
