# Household Management Agent

## Project Overview - Household Management Agent

**NOTE**: This is a submission for the [Kaggle Agents Intensive Capstone project](https://www.kaggle.com/competitions/agents-intensive-capstone-project/).

This project contains a multi-agent system designed to help homeowners manage household maintenance tasks intelligently. The agent is built using Google Agent Development Kit (ADK) and follows a modular architecture that coordinates specialized sub-agents to research, analyze, and compile comprehensive household maintenance recommendations.

### Problem Statement

Homeowners struggle to keep track of multiple maintenance responsibilities across appliances, seasonal yard work, and routine home care. Forgetting maintenance schedules can lead to costly repairs, reduced appliance lifespan, and safety hazards. The challenge is compounded by:

- **Information Overload**: Each appliance has different maintenance requirements and schedules
- **Seasonal Complexity**: Different maintenance tasks are required throughout the year based on local climate
- **Historical Context**: Past maintenance records are scattered and not used to predict future needs
- **Time Investment**: Manually researching and tracking all maintenance tasks is time-consuming

Without a centralized system, homeowners often react to problems rather than preventing them, leading to higher costs and avoidable emergencies.

### Solution Statement

The Household Management Agent automates the entire process of household maintenance planning by:

- **Intelligent Appliance Tracking**: Automatically retrieves appliance information via MCP (Model Context Protocol) and researches manufacturer-recommended maintenance schedules
- **Predictive Analysis**: Analyzes historical maintenance data to predict future maintenance needs and optimal service dates
- **Seasonal Awareness**: Researches location-specific seasonal maintenance tasks based on current date and local climate zone
- **Coordinated Research**: Leverages multiple specialized agents working in parallel to gather comprehensive information efficiently
- **Actionable Output**: Delivers a consolidated, prioritized task list with specific dates and recommendations

This transforms household maintenance from a reactive scramble into a proactive, organized system.

### Architecture

The Household Management Agent is a sophisticated multi-agent system where specialized agents collaborate to deliver comprehensive maintenance recommendations. The central orchestrator is the `HouseholdRootAgent`.

#### Agent Hierarchy

```
HouseholdRootAgent
└── SequentialResearchAggregator
    ├── ParallelResearchAgent
    │   ├── AppliancesAgent
    │   └── SeasonalAgent
    └── AggregatorAgent
```

#### Core Components

**Root Orchestrator: `root_agent`**

The `HouseholdRootAgent` is the main entry point, built using the `Agent` class from Google ADK. It coordinates the entire workflow by delegating tasks to the `SequentialResearchAggregator`, which manages the research and aggregation process. The root agent uses Gemini 2.5 Flash for its reasoning capabilities and includes retry logic for robustness.

**Research Coordinator: `start_agent` (SequentialResearchAggregator)**

This `SequentialAgent` orchestrates the research process in two phases:
1. Parallel research gathering via `ParallelResearchAgent`
2. Aggregation of findings via `AggregatorAgent`

**Parallel Research Team: `research_agent`**

The `ParallelAgent` enables simultaneous execution of specialized research agents, maximizing efficiency:

- **AppliancesAgent**: The most complex sub-agent, responsible for:
  - Retrieving appliance inventory from MCP toolset
  - Parsing appliance data (make, model, install date, maintenance history)
  - Researching maintenance recommendations via Google Search
  - Analyzing maintenance history patterns via `maintenance_analyzer_tool`
  - Coordinating findings into appliance-specific recommendations

- **SeasonalAgent**: Focuses on time-sensitive tasks by:
  - Determining current season and upcoming seasonal transitions
  - Researching location-specific maintenance (using zip code)
  - Identifying critical dates (frost dates, planting zones, etc.)
  - Compiling seasonal home care recommendations

**Aggregation Specialist: `aggregator_agent`**

This lightweight agent combines outputs from parallel research agents into a unified, readable format without modifying the content, preserving the structured recommendations from both appliance and seasonal research streams.

#### Supporting Agents

**Google Search Agent: `google_search_agent`**

A utility agent that performs targeted web searches and returns concise summaries. Used by multiple other agents to gather maintenance guidance and best practices. Built with Gemini 2.5 Flash Lite for cost-efficient search operations.

**Maintenance Analyzer Agent: `maintenance_analyzer_agent`**

Analyzes historical maintenance records to predict future needs. This agent:
- Processes maintenance date history from appliance records
- Identifies maintenance patterns and frequencies
- Uses Google Search to research typical maintenance intervals
- Generates predicted maintenance dates in standardized format (mm/dd/yyyy)
- Flags appliances lacking sufficient historical data

### Essential Tools and Utilities

**MCP Toolset Integration (`mcp_tool`)**

The project leverages Model Context Protocol to connect with an external household data service:
- **Endpoint**: `https://twixed.net/mcp/kaggle`
- **Configuration**: Read-only access to all toolsets
- **Purpose**: Retrieves appliance inventory and maintenance history in JSON format
- **Transport**: Streamable HTTP Server connection

**Agent Tools (`google_search_tool`, `maintenance_analyzer_tool`)**

These `AgentTool` wrappers enable agents to delegate specialized tasks:
- `google_search_tool`: Wraps `google_search_agent` for reusable search capability
- `maintenance_analyzer_tool`: Wraps `maintenance_analyzer_agent` for maintenance prediction

**Utility Functions (`get_zip_code_tool`)**

Provides location context for seasonal research. Currently returns a hardcoded zip code ("22015") but can be extended to dynamically determine user location.

**Configuration Management (`config.py`)**

The `ProjectConfig` dataclass centralizes all configuration:
- Model selection: Gemini 2.5 Flash for complex reasoning, Flash Lite for simple tasks
- Retry logic: Exponential backoff with 5 attempts for handling rate limits and transient failures
- HTTP status handling: 429, 500, 503, 504

### Workflow

The `HouseholdRootAgent` follows this workflow:

1. **Initialization**: User requests a household maintenance task list
2. **Parallel Research**: The system simultaneously:
   - **Appliance Research**: 
     - Retrieves appliance data from MCP
     - Extracts individual appliance records
     - Researches maintenance needs for each appliance
     - Analyzes maintenance history and predicts future tasks
   - **Seasonal Research**:
     - Determines current season and location
     - Researches seasonal maintenance tasks
     - Identifies critical dates and zone-specific needs
3. **Aggregation**: Combines research findings into a unified report
4. **Output Delivery**: Returns structured task list organized by:
   - Appliance-specific maintenance (grouped by appliance, ordered by date)
   - Seasonal maintenance tasks (with important dates highlighted)

### Value Statement

The Household Management Agent saves homeowners significant time and prevents costly repairs by:

- **Proactive Maintenance**: Predicts when appliances need service before breakdowns occur
- **Time Savings**: Eliminates hours of manual research across different appliance manuals and seasonal guides
- **Cost Prevention**: Reduces emergency repair costs through preventive maintenance
- **Comprehensive Coverage**: Ensures no maintenance task is overlooked across appliances and seasonal needs
- **Historical Learning**: Uses past maintenance data to improve future predictions

**Future Enhancements**:
- Integration with home automation systems for automatic scheduling
- Calendar integration to send maintenance reminders
- Cost estimation for upcoming maintenance tasks
- Priority scoring based on appliance age, failure risk, and maintenance urgency
- Multi-home support for property managers

## Installation

This project was built against Python 3.11+.

It is suggested you create a virtual environment using your preferred tooling (e.g., `venv`, `uv`, `conda`).

Install dependencies:
```bash
pip install google-adk
```

Additional requirements:
- Google Cloud credentials for Gemini API access
- Access to MCP endpoint (configured in `mcp.py`)

### Running the Agent in ADK Web Mode

From the command line of the working directory, execute:

```bash
adk web
```

Example interaction:
```
User: Assemble a task list of household duties for me.
Agent: [Retrieves appliances, researches maintenance, analyzes history, compiles seasonal tasks]
```

## Project Structure

The project is organized as follows:

- **`household_agent/`**: The main Python package for the agent
  - **`agent.py`**: Defines the `root_agent` and orchestrates the agent hierarchy
  - **`config.py`**: Contains configuration (model selection, retry options)
  - **`mcp.py`**: Configures the MCP toolset connection
  - **`tools.py`**: Defines custom tools and agent wrappers
  - **`sub_agents/`**: Contains specialized sub-agents
    - **`appliances_agent.py`**: Manages appliance research and maintenance analysis
    - **`seasonal_agent.py`**: Handles seasonal maintenance research
    - **`aggregator_agent.py`**: Combines research findings
    - **`google_search_agent.py`**: Performs web searches
    - **`maintenance_analyzer_agent.py`**: Analyzes maintenance history and predicts future needs
- **`LICENSE`**: Apache 2.0 license
- **`README.md`**: This file

## Conclusion

The Household Management Agent demonstrates how multi-agent systems, powered by Google's Agent Development Kit, can solve complex real-world problems through intelligent coordination. By breaking down household maintenance planning into specialized tasks—appliance research, seasonal awareness, historical analysis, and aggregation—the system creates a workflow that is efficient, scalable, and comprehensive.

The modular architecture allows each agent to focus on its domain expertise while the orchestration layer ensures seamless collaboration. The use of parallel execution for independent research tasks, combined with sequential aggregation, optimizes both performance and result quality. This design pattern can be extended to many other household management scenarios beyond maintenance planning.