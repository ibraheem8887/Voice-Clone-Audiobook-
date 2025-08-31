# audio_to_text.py (with detailed logs)

import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment

def audio_to_text(audio_file, output_txt=None):
    """
    Convert audio (wav/mp3/m4a/webm) to text as a whole file (no chunks).
    Added detailed logs to debug failures.
    """
    recognizer = sr.Recognizer()
    if output_txt is None:
        output_txt = os.path.join(tempfile.gettempdir(), "book_text.txt")

    temp_wav = os.path.join(tempfile.gettempdir(), "temp_whole.wav")

    print("🚀 Starting audio_to_text...")
    print(f"🎵 Input file: {audio_file}")
    print(f"📦 Exists? {os.path.exists(audio_file)}")
    if os.path.exists(audio_file):
        print(f"📏 File size: {os.path.getsize(audio_file) / 1024:.2f} KB")

    try:
        # ✅ Step 1: Load audio via pydub
        try:
            sound = AudioSegment.from_file(audio_file)
            print(f"🔊 Loaded audio: {len(sound)/1000:.2f} sec, "
                  f"Channels={sound.channels}, Rate={sound.frame_rate}")
        except Exception as e:
            print(f"❌ Step 1 FAILED: Could not decode audio: {e}")
            return None

        # ✅ Step 2: Normalize to WAV 16kHz mono
        try:
            sound = sound.set_frame_rate(16000).set_channels(1)
            sound.export(temp_wav, format="wav")
            print(f"✅ Step 2: Exported normalized audio -> {temp_wav} "
                  f"({os.path.getsize(temp_wav)/1024:.2f} KB)")
        except Exception as e:
            print(f"❌ Step 2 FAILED: Could not export normalized audio: {e}")
            return None

        # ✅ Step 3: Send to SpeechRecognition
        try:
            with sr.AudioFile(temp_wav) as source:
                audio = recognizer.record(source)
            print("✅ Step 3: Audio loaded into recognizer")
        except Exception as e:
            print(f"❌ Step 3 FAILED: Could not read audio into recognizer: {e}")
            return None

        # ✅ Step 4: Google API
        try:
            text = recognizer.recognize_google(audio)
            print("✅ Step 4: Google API returned text")
        except sr.UnknownValueError:
            print("⚠️ Step 4: Google could not understand the audio")
            text = ""
        except sr.RequestError as e:
            print(f"❌ Step 4 FAILED: Google API request error: {e}")
            return None
        except Exception as e:
            print(f"❌ Step 4 FAILED: Unexpected error calling Google API: {e}")
            return None

        # ✅ Step 5: Save transcript
        try:
            with open(output_txt, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"✅ Step 5: Transcript saved at {output_txt}")
        except Exception as e:
            print(f"❌ Step 5 FAILED: Could not save transcript: {e}")
            return None

        if text.strip():
            print("🎉 SUCCESS: Transcription complete")
            return output_txt
        else:
            print("⚠️ No text detected in audio")
            return None

    finally:
        if os.path.exists(temp_wav):
            try:
                os.remove(temp_wav)
                print("🧹 Temp file cleaned up")
            except Exception as e:
                print(f"⚠️ Cleanup failed: {e}")
