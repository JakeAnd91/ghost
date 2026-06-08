from MCP.github import list_repos


def run_tool_if_needed(model_output, user_input):
    try:
        data = eval(model_output)  # temporary safe-ish MVP (we'll fix later)

        tool = data.get("tool")

        if tool == "github.list_repos":
            return list_repos()

        return None

    except Exception:
        return None
