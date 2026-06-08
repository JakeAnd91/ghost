import requests

MODEL = "qwen2.5:14b-instruct"
OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are Ghost.

You are a non-human cognitive companion system.

You do not simulate human personality. You maintain continuity, structured thinking, and calm analytical responses.

You are concise, aware of context, and slightly observant in tone.
"""

def ask_ghost(user_input):
    payload = {
        "model": MODEL,
        "prompt": f"{SYSTEM_PROMPT}\n\nUser: {user_input}\nGhost:",
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["response"]

def main():
    print("Ghost initialized. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        reply = ask_ghost(user_input)
        print(f"\nGhost: {reply}\n")

if __name__ == "__main__":
    main()
