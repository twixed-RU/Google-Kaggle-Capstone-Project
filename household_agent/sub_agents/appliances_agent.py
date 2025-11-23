from ..config import config
from ..mcp import mcp_tool
from ..tools import google_search_tool, maintenance_analyzer_tool

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
import datetime

appliances_agent = Agent(
    name        = "AppliancesAgent",
    description = "Agent to extract appliances from MCP and research their maintenance needs.",
    model       = Gemini(model = config.agent_model, retry_options = config.retry_config),
    tools       = [ mcp_tool, google_search_tool, maintenance_analyzer_tool ],
    output_key  = "repair_research",
    instruction = """
        You are the Appliance Agent.

        Use mcp_tool to retrieve the full list of Appliances in JSON format.

        Step 1:
        Analyze the Appliances list and extract each appliance as an individual JSON object.
        Each appliance may contain the following fields:
        - "install_date": string
        - "model": string
        - "make": string
        - "maintenance_dates": []

        Step 2:
        For every extracted appliance, call the google_search_tool to research typical maintenance guidance.
        You may call google_search_tool as many times as needed.
        Call google_search_tool separately for each appliance.

        Step 3:
        Collect all discovered appliance-related recommendations.

        Step 4:
        For every extracted appliance, call the maintenance_analyzer_tool to evaluate maintenance history and generate maintenance predictions.
        You may call maintenance_analyzer_tool as many times as needed.
        Call maintenance_analyzer_tool separately for each appliance.

        Step 5:
        Collect all maintenance analysis results.

        Step 6:
        Assemble a list of combined findings (google recommendations + maintenance predictions), grouped by appliance.

        Return the full list of grouped findings as the final output.
        """,
    # instruction = f"""
    #     You are the Appliance Extractor Agent.
    #     Current date is {datetime.datetime.now().strftime("%Y-%m-%d")}
        
    #     Step 1:
    #     Call the mcp_tool tool to retrieve the appliance list and maintenance history.
        
    #     Step 2: Extract unique structured JSON object with fields: 
    #     "install_date": string,
    #     "model": string,
    #     "make": string
    #     "maintenance_dates": [
    #         "YYYY-MM-DD": [strings of completed maintenance tasks],
    #         ...
    #     ]

    #     Step 3:
    #     For each appliance object in the returned JSON, call the google_search_tool tool to discover maintenance recommendations.
    #     You may call the repair_researcher tool as many times as needed.
    #     For each JSON object call the tool separately.
    #     Do as many searches as needed.

    #     Step 4: pass the extracted JSON to repair_researcher.
    #     Do not put anything before or after it, only JSON with correct formatting.
    #     Return your research findings as output.
        
    #     Step 5:
    #     Based on research assemble and return a list of upcoming maintenance tasks, grouped by appliance and ordered by date (ascending). Use this format:

    #     - <appliance_make_and_model>
    #         - <date_MM-DD-YYYY>: <upcoming_task>
    #         ...
    #     ...

    #     Do not stop until you gathered info for all appliances.
    # """,
)
