import datetime
from google.genai import types
from dataclasses import dataclass

@dataclass
class ProjectConfig:
    project_name: str    = "HouseholdAgent"
    project_version: str = "1.0.0"
    agent_model: str     = "gemini-2.5-flash-lite"
    retry_config         = types.HttpRetryOptions(
        attempts          = 5,
        exp_base          = 7,
        initial_delay     = 1,
        http_status_codes = [ 429, 500, 503, 504 ]
    )

config = ProjectConfig()