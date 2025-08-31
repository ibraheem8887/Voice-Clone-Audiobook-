# audio_to_text.py (No Chunking, Full Audio at Once)
import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment

def audio_to_text(audio_file, output_txt=None):
    """
    Convert an audio file (wav/mp3/m4a/webm) to text as a single block.
    Uses Google SpeechRecognition API.
    """
    recognizer = sr.Recognizer()
    if output_txt is None:
        output_txt = os.path.join(tempfile.gettempdir(), "book_text.txt")

    temp_wav = os.path.join(tempfile.gettempdir(), "temp_full.wav")

    try:
        # ✅ Normalize audio: convert to mono 16kHz WAV
        try:
            sound = AudioSegment.from_file(audio_file)
            sound = sound.set_frame_rate(16000).set_channels(1)
            sound.export(temp_wav, format="wav")
        except Exception as e:
            print(f"❌ Could not decode/convert audio file: {e}")
            return None

        # ✅ Process full audio in one shot
        with sr.AudioFile(temp_wav) as source:
            audio = recognizer.record(source)  # no chunking, grab all

        try:
            full_text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("⚠️ Speech not understood in audio.")
            full_text = ""
        except sr.RequestError as e:
            print(f"❌ API request error: {e}")
            full_text = ""

        # ✅ Write transcript (even if empty, so pipeline doesn’t break)
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
            print("⚠️ No speech detected in audio.")
            return None

    finally:
        # ✅ Cleanup temp file
        if os.path.exists(temp_wav):
            try:
                os.remove(temp_wav)
            except Exception as e:
                print(f"⚠️ Could not delete temp file: {e}")
