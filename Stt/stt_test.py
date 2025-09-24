import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import torch

# ==== SETTINGS ====
DURATION = 5          # seconds to record
SAMPLE_RATE = 16000   # standard sample rate for Whisper
DEVICE = "cpu"


# ==== LOAD MODEL ONCE ====
print("Loading Whisper model...")
model = WhisperModel("small", device=DEVICE)
print(f"Model loaded on {DEVICE}.")

# ==== RECORD AUDIO ====
print(f"Recording for {DURATION} seconds...")
audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype=np.float32)
sd.wait()
print("Recording finished.")

# Flatten audio to 1D array for Whisper
audio = audio.flatten()

# ==== TRANSCRIBE ====
print("Transcribing audio...")
segments, _ = model.transcribe(audio, beam_size=5)
transcript = " ".join([seg.text for seg in segments])

print("\n🎤 Transcript:")
print(transcript)
