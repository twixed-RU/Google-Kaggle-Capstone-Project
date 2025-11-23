from ..config import config
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

import datetime

maintenance_analyzer_agent = Agent(
    name        = "maintenance_analyzer_agent",
    model       = Gemini(model = config.agent_model, retry_options = config.retry_config),
    tools       = [ google_search ],
    output_key  = "google_search_results",
    instruction = """
        You are smart Maintenance Analyzer Agent.
        You can find current date here {datetime.datetime.now().strftime("%Y-%m-%d")}
        You will receive JSON object. You will work only with "maintenance_dates" field.
        If object don't have "maintenance_dates" field return message "Don't have enough data to analyze"
        Analyze "maintenance_dates" value and predict future maintenance tasks and dates.
        Use the google_search tool if needed to research typical maintenance schedules.
        Return a concise summary of the findings with proposed maintenance tasks and dates with format mm/dd/yyyy. 

    """,
)
