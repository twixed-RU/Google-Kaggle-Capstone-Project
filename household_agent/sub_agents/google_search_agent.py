from ..config import config
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

google_search_agent = Agent(
    name        = "GoogleSearchAgent",
    model       = Gemini(model = config.agent_model_lite, retry_options = config.retry_config),
    tools       = [ google_search ],
    output_key  = "google_search_results",
    instruction = """
        You are the Google Search Agent.
        Search for what is asked and return a concise summary of the findings.
        Use the google_search tool to perform searches.
    """,
)
