from MCP.tools.filesystem import read_rdpa_journals
from MCP.tools.github import list_repos


TOOLS = {
    "filesystem.read_rdpa_journals": read_rdpa_journals,
    "github.list_repos": list_repos,
}


def run_tool(tool_name, args=None):
    args = args or {}

    if tool_name not in TOOLS:
        return f"Unknown tool: {tool_name}"

    return TOOLS[tool_name](**args)
