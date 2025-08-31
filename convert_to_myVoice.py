import os
import sys
import time
import shutil
import tempfile
import io
from TTS.api import TTS

# Force UTF-8 for prints
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding="utf-8")


def true_voice_cloning():
    # Config
    INPUT_TEXT = "book_text.txt"
    VOICE_FILE = "myVoice/myVoice.wav"
    TMP_DIR = tempfile.mkdtemp()
    CHUNK_SIZE = 400

    print("🎯 VOICE CLONING WITH YOUR VOICE")
    print("=" * 50)

    # Verify input files
    if not os.path.exists(INPUT_TEXT):
        print(f"❌ Error: {INPUT_TEXT} not found!")
        return False

    if not os.path.exists(VOICE_FILE):
        print(f"❌ Error: {VOICE_FILE} not found!")
        return False

    # Read text file
    try:
        with open(INPUT_TEXT, "r", encoding="utf-8") as f:
            full_text = f.read()
        print(f"📖 Read {len(full_text)} characters")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

    # Split text into chunks
    words = full_text.split()
    chunks = [" ".join(words[i : i + CHUNK_SIZE]) for i in range(0, len(words), CHUNK_SIZE)]
    print(f"✂️  Split into {len(chunks)} chunks")

    # Load TTS model
    try:
        print("🔊 Loading YourTTS model (this may take a while)...")
        # Clear old corrupted model if exists
        model_path = os.path.expanduser("~/.local/share/tts/tts_models--multilingual--multi-dataset--your_tts")
        if os.path.exists(model_path):
            shutil.rmtree(model_path)
            print("🧹 Cleared old model files")

        tts = TTS("tts_models/multilingual/multi-dataset/your_tts", gpu=False)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False

    # Test with small sentence
    try:
        print("🧪 Testing voice cloning...")
        test_path = os.path.join(TMP_DIR, "test_my_voice.wav")
        tts.tts_to_file(
            text="This is a voice cloning test with my voice.",
            speaker_wav=VOICE_FILE,
            language="en",
            file_path=test_path,
        )
        print("✅ Test audio generated!")
    except Exception as e:
        print(f"❌ Voice test failed: {e}")
        return False

    # Process all chunks
    print(f"\n🎵 Creating {len(chunks)} chunks with YOUR voice...")
    audio_buffers = []
    successful = 0

    for i, chunk in enumerate(chunks, 1):
        try:
            out_path = os.path.join(TMP_DIR, f"chunk_{i}.wav")
            tts.tts_to_file(text=chunk, speaker_wav=VOICE_FILE, language="en", file_path=out_path)

            # Load back into memory (BytesIO)
            with open(out_path, "rb") as f:
                audio_bytes = f.read()
            audio_buffers.append(io.BytesIO(audio_bytes))

            successful += 1
            print(f"✅ Saved chunk {i}/{len(chunks)}")
        except Exception as e:
            print(f"❌ Failed chunk {i}: {e}")
            continue

        time.sleep(0.5)

    print(f"\n{'='*50}")
    if successful > 0:
        print(f"🎉 Created {successful} chunks with YOUR VOICE!")
        print(f"📁 Temporary dir: {TMP_DIR}/")
        print("➡️  Merge chunks in Streamlit using BytesIO + pydub")
        return audio_buffers  # return list of BytesIO chunks
    else:
        print("❌ No chunks created")
        print("💡 This is likely due to Python version incompatibility")
        print("   TTS requires Python 3.9-3.11, but this is Python 3.13.6")
        print("   Add a 'runtime.txt' file with: python-3.11.9")
        return False


if __name__ == "__main__":
    true_voice_cloning()
