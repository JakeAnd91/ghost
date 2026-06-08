memory_buffer = []
memory_summary = ""

MAX_BUFFER = 8


def build_context():
    buffer_text = "\n".join(memory_buffer)

    return f"""
[Memory Summary]
{memory_summary}

[Recent Memory]
{buffer_text}
"""


def update_memory(user, ghost):
    global memory_buffer

    memory_buffer.append(f"User: {user}")
    memory_buffer.append(f"Ghost: {ghost}")

    if len(memory_buffer) > MAX_BUFFER:
        memory_buffer = memory_buffer[-MAX_BUFFER:]
