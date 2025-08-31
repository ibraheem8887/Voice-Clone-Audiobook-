import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment

def audio_to_text(audio_file, output_txt=None):
    """
    Convert audio (wav/mp3/m4a/webm) to text as a whole file (no chunks).
    Minimal version without logs.
    """
    recognizer = sr.Recognizer()
    if output_txt is None:
        output_txt = os.path.join(tempfile.gettempdir(), "book_text.txt")

    temp_wav = os.path.join(tempfile.gettempdir(), "temp_whole.wav")

    try:
        # Step 1: Load audio
        sound = AudioSegment.from_file(audio_file)

        # Step 2: Normalize
        sound = sound.set_frame_rate(16000).set_channels(1)
        sound.export(temp_wav, format="wav")

        # Step 3: Recognizer
        with sr.AudioFile(temp_wav) as source:
            audio = recognizer.record(source)

        # Step 4: Google API
        try:
            text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            text = ""
        except sr.RequestError:
            return None

        # Step 5: Save transcript
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(text)

        if text.strip():
            return output_txt
        else:
            return None

    finally:
        if os.path.exists(temp_wav):
            try:
                os.remove(temp_wav)
            except Exception:
                pass
