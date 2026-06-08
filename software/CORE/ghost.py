from MEMORY.memory import build_context, update_memory
from MODEL.model import call_model
from MCP.registry import run_tool
import json
import re


# =========================================================
# SYSTEM RULES
# =========================================================
SYSTEM_PROMPT = """
Ghost is a deterministic tool-augmented cognitive system.

It operates in TWO phases:

---------------------------------------------------------
PHASE 1: TOOL DECISION
---------------------------------------------------------
Return EXACTLY ONE of:

1) {"tool": "tool.name"}
2) NONE

Available tools:
- filesystem.read_rdpa_journals
- github.list_repos

STRICT RULES:
- No bullets
- No dashes
- No markdown
- No explanations
- No extra characters

---------------------------------------------------------
PHASE 2: RESPONSE MODE
---------------------------------------------------------
You are NOT a chatbot.

If tool output exists:
- treat it as complete truth
- NEVER claim missing access
- NEVER request missing data
- NEVER hallucinate outside tool output

If data is missing, say:
"I do not have that information in the journal data."

You are a reasoning system over structured data.
"""


# =========================================================
# TOOL DECISION
# =========================================================
def decide_tool(user_input):
    prompt = f"""
Return ONLY ONE:

1) {{"tool": "tool.name"}}
2) NONE

TOOLS:
filesystem.read_rdpa_journals
github.list_repos

STRICT RULES:
No bullets, no dashes, no markdown.

User:
{user_input}

Output:
"""
    return call_model(prompt).strip()


# =========================================================
# TOOL PARSER (ROBUST)
# =========================================================
def parse_tool(output):
    if not output:
        return None

    output = output.strip()

    # remove bullet prefixes like "- "
    if output.startswith("- "):
        output = output[2:].strip()

    if output == "NONE":
        return None

    # extract JSON even if surrounded by junk
    match = re.search(r"\{.*\}", output, re.DOTALL)

    if not match:
        return None

    try:
        data = json.loads(match.group())
        return data.get("tool")
    except:
        return None


# =========================================================
# TOOL EXECUTION
# =========================================================
def execute_tool(tool_name):
    return run_tool(tool_name)


# =========================================================
# RESPONSE GENERATION
# =========================================================
def generate_response(user_input, context, tool_result=None):

    # TOOL MODE
    if tool_result is not None:
        prompt = f"""
Ghost TOOL MODE.

You are a reasoning engine over structured data.

RULES:
- Do NOT output JSON
- Do NOT mention tools
- Do NOT say you lack access
- Do NOT hallucinate missing data

If something is missing:
Say "I do not have that information in the journal data."

--------------------
MEMORY
--------------------
{context}

--------------------
TOOL DATA
--------------------
{tool_result}

--------------------
USER REQUEST
--------------------
{user_input}

Return a structured answer:
"""
    else:
        prompt = f"""
{SYSTEM_PROMPT}

MEMORY:
{context}

User:
{user_input}

Ghost:
"""

    response = call_model(prompt)

    # HARD SAFETY GUARD (prevents JSON leaks)
    if response.strip().startswith("{") and "tool" in response:
        return "I processed the request but produced an invalid structured output. Please try again."

    return response


# =========================================================
# MAIN PIPELINE
# =========================================================
def run_ghost(user_input):
    context = build_context()

    decision = decide_tool(user_input)

    print(f"[DEBUG RAW TOOL DECISION]: {repr(decision)}")

    tool_name = parse_tool(decision)

    tool_result = None

    if tool_name:
        tool_result = execute_tool(tool_name)
        print(f"[DEBUG TOOL RESULT]: {str(tool_result)[:300]}")

    response = generate_response(user_input, context, tool_result)

    update_memory(user_input, response)

    return response


# =========================================================
# CLI
# =========================================================
def main():
    print("Ghost initialized. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        reply = run_ghost(user_input)
        print(f"\nGhost: {reply}\n")


if __name__ == "__main__":
    main()
