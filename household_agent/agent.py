from .sub_agents.appliances_agent import appliances_agent
from .sub_agents.aggregator_agent import aggregator_agent
from .sub_agents.seasonal_agent import seasonal_agent
from .config import config
from google.adk.agents import ParallelAgent, SequentialAgent, Agent
from google.adk.models.google_llm import Gemini

research_agent = ParallelAgent(
    name       = "ParallelResearchAgent",
    sub_agents = [ appliances_agent, seasonal_agent ],
)

start_agent = SequentialAgent(
    name        = "SequentialResearchAggregator",
    description = "Agent to research household maintenance tasks and aggregate findings.",
    sub_agents  = [ research_agent, aggregator_agent ],
)


root_agent = Agent(
    name        = "HouseholdRootAgent",
    model       = Gemini(model = config.agent_model, retry_options = config.retry_config),
    sub_agents  = [ start_agent ],
    instruction = """
        You are the Household Management Root Agent.
        Your task is to coordinate sub-agents to assemble a comprehensive household maintenance task list.
        Begin by instructing the SequentialResearchAggregator to perform research and aggregate findings.
        Finally, compile a clear and concise summary of all household duties.
    """,
)