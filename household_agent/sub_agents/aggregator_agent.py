from ..config import config
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
import datetime

aggregator_agent = Agent(
    name        = "AggregatorAgent",
    model       = Gemini(model = config.agent_model_lite, retry_options = config.retry_config),
    instruction = f"""
        Current date is {datetime.datetime.now().strftime("%Y-%m-%d")}
        Collect these two research findings into a single output without changing anything:
    
        **Seasonal Tasks:**
        {{seasonal_research}}
        
        **Possible repairs:**
        {{repair_research}}
    """,
)