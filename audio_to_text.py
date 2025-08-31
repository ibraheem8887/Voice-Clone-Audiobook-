# audio_to_text.py (Cloud + Streamlit friendly)
import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment

def audio_to_text(audio_file, output_txt=None, chunk_length_ms=60000):
    """
    Convert audio (wav/mp3) to text with chunking.
    - audio_file: uploaded audio file path
    - output_txt: save transcript file path (defaults to /tmp/book_text.txt)
    - chunk_length_ms: length of chunks in ms (default 60 sec)
    """
    recognizer = sr.Recognizer()
    if output_txt is None:
        output_txt = os.path.join(tempfile.gettempdir(), "book_text.txt")

    try:
        # ✅ Always convert to mono 16kHz WAV for best results
        sound = AudioSegment.from_file(audio_file)
        sound = sound.set_frame_rate(16000).set_channels(1)

        text_result = []
        temp_wav = os.path.join(tempfile.gettempdir(), "temp_chunk.wav")

        # ✅ Process audio in chunks (1 minute each)
        for i, chunk in enumerate(sound[::chunk_length_ms]):
            chunk.export(temp_wav, format="wav")
            with sr.AudioFile(temp_wav) as source:
                audio = recognizer.record(source)

                try:
                    chunk_text = recognizer.recognize_google(audio)
                    text_result.append(chunk_text)
                    print(f"Chunk {i+1} transcribed.")
                except sr.UnknownValueError:
                    print(f"⚠️ Chunk {i+1}: could not understand audio.")
                except sr.RequestError as e:
                    print(f"❌ API request error on chunk {i+1}: {e}")

        full_text = "\n".join(text_result)

        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"✅ Transcription saved: {output_txt}")
        return output_txt if full_text.strip() else None

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None
    finally:
        if os.path.exists(temp_wav):
            os.remove(temp_wav)
