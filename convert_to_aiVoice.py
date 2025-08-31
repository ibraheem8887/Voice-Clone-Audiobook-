# file: gtts_audiobook_fast.py

import os
import sys
import time
import io
from gtts import gTTS

sys.stdout.reconfigure(encoding="utf-8")

TEXT_FILE = "book_text.txt"


def read_text(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found!")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def text_to_speech_fast(text, output_file):
    print("🔊 Starting audiobook conversion for entire book...")

    start_time = time.time()
    tts = gTTS(text=text, lang="en")
    tts.save(output_file)  # Save locally for compatibility

    elapsed = time.time() - start_time
    print(f"✅ Audiobook completed and saved as {output_file}")
    print(f"⏱ Total time taken: {int(elapsed // 60)} min {int(elapsed % 60)} sec")

    # Also return as in-memory bytes (for Streamlit)
    bio = io.BytesIO()
    tts.write_to_fp(bio)
    bio.seek(0)
    return bio


if __name__ == "__main__":
    full_text = read_text(TEXT_FILE)
    audio_bytes = text_to_speech_fast(full_text, OUTPUT_AUDIO)
