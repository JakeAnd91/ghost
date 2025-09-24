# import
import sys
from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=False)

ghost_ref = "ghost_clip.wav"

def main():
    while True:
        text = input("Say Hi to Ghost (or 'quit' to end): ")
        if text.lower() == "quit":
            break
        if not text.strip():
            continue

        tts.tts_to_file(
            text=text,
            speaker_wav=ghost_ref,
            language="en",
            file_path= "ghost_clip_output.wav",
            decoder_max_step=500  # prevents runaway decoding
        )

main()
 