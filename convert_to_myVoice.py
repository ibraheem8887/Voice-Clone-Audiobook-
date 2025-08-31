import os
import tempfile
from TTS.api import TTS

def true_voice_cloning(text_file, voice_file, tmp_dir=None, chunk_size=400):
    """
    Clone your voice and return a list of audio chunks (in-memory bytes).
    """

    if tmp_dir is None:
        tmp_dir = tempfile.mkdtemp()

    if not os.path.exists(text_file):
        raise FileNotFoundError(f"❌ Text file not found: {text_file}")
    if not os.path.exists(voice_file):
        raise FileNotFoundError(f"❌ Voice sample not found: {voice_file}")

    # Load text
    with open(text_file, "r", encoding="utf-8") as f:
        full_text = f.read()

    # Split text into chunks
    words = full_text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

    # Load TTS model
    tts = TTS("tts_models/multilingual/multi-dataset/your_tts", gpu=False)

    # Generate chunks
    audio_chunks = []
    for i, chunk in enumerate(chunks):
        out_path = os.path.join(tmp_dir, f"chunk_{i}.wav")
        tts.tts_to_file(text=chunk, file_path=out_path, speaker_wav=voice_file, language="en")
        with open(out_path, "rb") as f:
            audio_chunks.append(f.read())

    return audio_chunks
