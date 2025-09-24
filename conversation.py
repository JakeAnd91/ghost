class ConversationManager:
    def __init__(self):
        self.history = []

    def get_response(self, user_text):
        # Add to history
        self.history.append({"role": "user", "content": user_text})

        # Placeholder response
        reply = f"I heard you say: '{user_text}'"

        self.history.append({"role": "assistant", "content": reply})
        return reply
