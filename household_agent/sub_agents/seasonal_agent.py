from ..config import config
from ..tools import google_search_tool, get_zip_code_tool
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
import datetime

seasonal_agent = Agent(
    name        = "SeasonalAgent",
    model       = Gemini(model = config.agent_model, retry_options = config.retry_config),
    tools       = [ get_zip_code_tool, google_search_tool ],
    output_key  = "seasonal_research",
    instruction = f"""
        Current date is {datetime.datetime.now().strftime("%Y-%m-%d")}
        Research home maintenance tasks for current and upcoming seasons.
        Use get_zip_code_tool to get the zip code if needed for location-specific information.
        Use google_search_tool to find relevant information.
        Underline important dates such as last frost dates or zone calendar ideas.
        Keep the report concise (200 words).
    """,
)
