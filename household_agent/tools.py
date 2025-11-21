from .sub_agents.google_search_agent import google_search_agent
from google.adk.tools import AgentTool

google_search_tool = AgentTool(google_search_agent)

def get_zip_code_tool() -> str:
    # In a real implementation, this would return a tool that provides the zip code.
    return "22015"
