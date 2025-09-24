class SpeechToText:
    def __init__(self):
        # Setup mic / model here
        pass

    def listen(self):
        """
        Capture audio from mic and return transcribed text.
        For now, just mock with input() so you can test AI + TTS separately.
        """
        return input("You: ")
