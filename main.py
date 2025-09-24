from stt_module import SpeechToText
from conversation import ConversationManager
from tts_module import TextToSpeech

def main():
    stt = SpeechToText()
    ai = ConversationManager()
    tts = TextToSpeech()

    print("Assistant running... (say 'quit' to stop)")

    while True:
        # 1. Listen
        user_text = stt.listen()
        if not user_text:
            continue

        if user_text.lower() in ["quit", "exit", "stop"]:
            print("Shutting down...")
            break

        # 2. Process AI response
        response = ai.get_response(user_text)
        print(f"AI: {response}")

        # 3. Speak back
        tts.speak(response)

if __name__ == "__main__":
    main()
