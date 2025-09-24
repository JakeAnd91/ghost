import subprocess
import tempfile
import simpleaudio as sa
import os

# ==== CONFIG ====
PIPER_PATH = r"C:\piper\piper.exe"  # raw string avoids backslash issues
PIPER_VOICE = r"C:\piper\voices\en_US-libritts_r-medium.onnx"  # known-good voice

def speak(text):
    tmp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name

    # Use shell=True + quoted paths
    command = f'"{PIPER_PATH}" --model "{PIPER_VOICE}" --output_file "{tmp_wav}" --text "{text}"'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)

    if result.returncode != 0:
        print("❌ Piper error:")
        print(result.stderr)  # should now show real error
        return

    if os.path.exists(tmp_wav):
        wave_obj = sa.WaveObject.from_wave_file(tmp_wav)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    else:
        print("❌ Piper did not produce a WAV file.")

# ==== TEST ====
if __name__ == "__main__":
    speak("Hello, Guardian! Welcome back.")
