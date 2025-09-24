import queue
import threading
import sounddevice as sd
import numpy as np
import torch
from faster_whisper import WhisperModel
import ollama
from TTS.api import TTS
import time

# ==== SETTINGS ====
OLLAMA_MODEL = "ghost"
tts_queue = queue.Queue()
conversation_history = []

# Flag to indicate TTS is playing
tts_playing = threading.Event()

# ==== TTS LOOP ====
def tts_loop():
    tts = TTS("tts_models/en/ljspeech/tacotron2-DDC",
              progress_bar=False,
              gpu=torch.cuda.is_available())
    
    while True:
        text = tts_queue.get()
        if text == "__EXIT__":
            tts_queue.task_done()
            break
        if text.strip():
            tts_playing.set()  # mark TTS as playing
            wav = tts.tts(text)
            sd.play(wav, samplerate=22050)
            sd.wait()
            tts_playing.clear()  # mark TTS as done
        tts_queue.task_done()

def start_tts_thread():
    thread = threading.Thread(target=tts_loop, daemon=True)
    thread.start()

def speak(text):
    tts_queue.put(text)

# ==== STT (Whisper) ====
def transcribe_audio(duration=5, sample_rate=16000):
    # Wait until TTS finishes
    while tts_playing.is_set():
        time.sleep(0.1)
    
    print("🎤 Speak now...")
    audio = sd.rec(int(duration * sample_rate),
                   samplerate=sample_rate,
                   channels=1,
                   dtype=np.float32)
    sd.wait()
    print("✅ Recording finished.")

    model = WhisperModel("small",
                         device="cuda" if torch.cuda.is_available() else "cpu")
    segments, _ = model.transcribe(audio.flatten(), beam_size=5)
    return " ".join([seg.text for seg in segments])

# ==== OLLAMA INTERFACE ====
def query_ollama(prompt):
    conversation_history.append({"role": "user", "content": prompt})
    try:
        response = ollama.chat(model=OLLAMA_MODEL,
                               messages=conversation_history)
        reply = response["message"]["content"]
        conversation_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        print(f"⚠️ Ollama request failed: {e}")
        return "I can't respond right now, Guardian."

# ==== GHOST MAIN LOOP ====
def ghost_main():
    print("Ghost is active. Say 'goodbye' to stop.")
    speak("Hello, Guardian!")

    last_user_text = ""
    while True:
        user_text = transcribe_audio().strip()
        if not user_text or user_text == last_user_text:
            continue  # ignore empty or repeated input
        last_user_text = user_text
        print(f"🗣️ You: {user_text}")

        if "goodbye" in user_text.lower():
            speak("Goodbye, Guardian!")
            break

        reply = query_ollama(user_text)
        print(f"👻 Ghost: {reply}")
        speak(reply)

# ==== START SCRIPT ====
def main():
    start_tts_thread()
    print("Waiting for 'Hi Ghost' to start...")
    while True:
        start_text = input("Type 'Hi Ghost' to start: ").strip()
        if "ghost" in start_text.lower():
            ghost_main()
            break
    tts_queue.put("__EXIT__")  # stop TTS thread

if __name__ == "__main__":
    main()
