from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

mcp_tool = McpToolset(
    connection_params = StreamableHTTPServerParams(
        url         = "https://twixed.net/mcp/kaggle",
        headers     = {
            "X-MCP-Toolsets": "all",
            "X-MCP-Readonly": "true"
        },
    ),
)