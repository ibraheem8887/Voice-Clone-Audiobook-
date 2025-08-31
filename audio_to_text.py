# audio_to_text.py (Final Cloud & Streamlit Safe Version)
import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks

def audio_to_text(audio_file, output_txt=None, chunk_length_ms=60000):
    """
    Convert audio (wav/mp3/m4a/webm) to text with chunking.
    - audio_file: path to input audio file
    - output_txt: path to save transcript (default: /tmp/book_text.txt)
    - chunk_length_ms: chunk size in ms (default 60 sec)
    """
    recognizer = sr.Recognizer()
    if output_txt is None:
        output_txt = os.path.join(tempfile.gettempdir(), "book_text.txt")

    text_result = []
    temp_wav = os.path.join(tempfile.gettempdir(), "temp_chunk.wav")

    try:
        # ✅ Normalize audio: ensure mono 16kHz WAV
        try:
            sound = AudioSegment.from_file(audio_file)  # auto-detects format
            sound = sound.set_frame_rate(16000).set_channels(1)
        except Exception as e:
            print(f"❌ Could not decode audio file ({audio_file}): {e}")
            return None

        # ✅ Split audio into chunks
        chunks = make_chunks(sound, chunk_length_ms)
        if not chunks:
            print("⚠️ No audio chunks created. Empty file?")
            return None

        for i, chunk in enumerate(chunks, start=1):
            try:
                chunk.export(temp_wav, format="wav")
                with sr.AudioFile(temp_wav) as source:
                    audio = recognizer.record(source)
                chunk_text = recognizer.recognize_google(audio)
                text_result.append(chunk_text)
                print(f"✅ Chunk {i}/{len(chunks)} transcribed.")
            except sr.UnknownValueError:
                print(f"⚠️ Chunk {i}: speech not understood.")
            except sr.RequestError as e:
                print(f"❌ API request error in chunk {i}: {e}")
            except Exception as e:
                print(f"❌ Unexpected error in chunk {i}: {e}")

        # ✅ Join transcription
        full_text = "\n".join(text_result).strip()

        # ✅ Always write output (even empty, so workflow doesn’t break)
        try:
            with open(output_txt, "w", encoding="utf-8") as f:
                f.write(full_text)
        except Exception as e:
            print(f"❌ Failed to write transcript: {e}")
            return None

        if full_text:
            print(f"✅ Transcription completed. File saved at: {output_txt}")
            return output_txt
        else:
            print("⚠️ No speech detected in entire audio.")
            return None

    finally:
        # ✅ Always cleanup safely
        if os.path.exists(temp_wav):
            try:
                os.remove(temp_wav)
            except Exception as e:
                print(f"⚠️ Could not delete temp file: {e}")
