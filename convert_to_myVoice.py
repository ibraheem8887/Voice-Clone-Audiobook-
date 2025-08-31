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


def true_voice_cloning(text_file, output_audio, voice_file="myVoice/myVoice.wav", chunk_size=400):
    """
    Clone your voice and generate audiobook from a text file.

    Args:
        text_file (str): Path to input text file.
        output_audio (str): Path for final merged audiobook (wav/mp3).
        voice_file (str): Path to your reference voice sample.
        chunk_size (int): Max words per chunk.
    """
    TMP_DIR = tempfile.mkdtemp()

    print("🎯 VOICE CLONING WITH YOUR VOICE")
    print("=" * 50)

    # Verify input files
    if not os.path.exists(text_file):
        print(f"❌ Error: {text_file} not found!")
        return False
    if not os.path.exists(voice_file):
        print(f"❌ Error: {voice_file} not found!")
        return False

    # Read text file
    try:
        with open(text_file, "r", encoding="utf-8") as f:
            full_text = f.read()
        print(f"📖 Read {len(full_text)} characters")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

    # Split text into chunks
    words = full_text.split()
    chunks = [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]
    print(f"✂️  Split into {len(chunks)} chunks")

    # Load TTS model
    try:
        print("🔊 Loading YourTTS model (this may take a while)...")
        model_path = os.path.expanduser("~/.local/share/tts/tts_models--multilingual--multi-dataset--your_tts")
        if os.path.exists(model_path):
            shutil.rmtree(model_path)
            print("🧹 Cleared old model files")

        tts = TTS("tts_models/multilingual/multi-dataset/your_tts", gpu=False)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False

    # Process chunks
    print(f"\n🎵 Creating {len(chunks)} chunks with YOUR voice...")
    all_wavs = []
    successful = 0

    for i, chunk in enumerate(chunks, 1):
        try:
            out_path = os.path.join(TMP_DIR, f"chunk_{i}.wav")
            tts.tts_to_file(text=chunk, speaker_wav=voice_file, language="en", file_path=out_path)
            all_wavs.append(out_path)
            successful += 1
            print(f"✅ Saved chunk {i}/{len(chunks)}")
        except Exception as e:
            print(f"❌ Failed chunk {i}: {e}")
            continue
        time.sleep(0.5)

    # Merge into single audiobook
    if successful > 0:
        try:
            from pydub import AudioSegment

            print("🔗 Merging chunks...")
            final_audio = AudioSegment.empty()
            for wav in all_wavs:
                final_audio += AudioSegment.from_wav(wav)
            final_audio.export(output_audio, format="mp3" if output_audio.endswith(".mp3") else "wav")

            print(f"🎉 Audiobook created: {output_audio}")
            return output_audio
        except Exception as e:
            print(f"❌ Merge failed: {e}")
            return all_wavs  # fallback: return list of chunk files
    else:
        print("❌ No chunks created")
        return False


if __name__ == "__main__":
    true_voice_cloning("book_text.txt", "book_audio.mp3")
