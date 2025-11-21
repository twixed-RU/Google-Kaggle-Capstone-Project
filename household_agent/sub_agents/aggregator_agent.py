from ..config import config
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
import datetime

aggregator_agent = Agent(
    name        = "AggregatorAgent",
    model       = Gemini(model = config.agent_model, retry_options = config.retry_config),
    instruction = f"""
        Current date is {datetime.datetime.now().strftime("%Y-%m-%d")}
        Combine these two research findings into a single summary:
    
        **Seasonal Tasks:**
        {{seasonal_research}}
        
        **Possible repairs:**
        {{repair_research}}
        
        Your summary should highlight common themes, connections, and the most important key takeaways from all reports. 
        The final summary should be around 200 words for seasonal tasks and a proper list of appliances and their upcoming maintenance schedule.
    """,
)