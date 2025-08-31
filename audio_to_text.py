import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks

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

    temp_wav = None   # ✅ Ensure always defined

    try:
        # ✅ Convert input audio to mono 16kHz WAV
        sound = AudioSegment.from_file(audio_file)
        sound = sound.set_frame_rate(16000).set_channels(1)

        # ✅ Split into proper time chunks
        chunks = make_chunks(sound, chunk_length_ms)

        text_result = []
        temp_wav = os.path.join(tempfile.gettempdir(), "temp_chunk.wav")

        for i, chunk in enumerate(chunks):
            # Export each chunk to temp WAV
            chunk.export(temp_wav, format="wav")
            with sr.AudioFile(temp_wav) as source:
                audio = recognizer.record(source)

                try:
                    chunk_text = recognizer.recognize_google(audio)
                    text_result.append(chunk_text)
                    print(f"✅ Chunk {i+1}/{len(chunks)} transcribed.")
                except sr.UnknownValueError:
                    print(f"⚠️ Chunk {i+1}: could not understand audio.")
                except sr.RequestError as e:
                    print(f"❌ API request error on chunk {i+1}: {e}")

        full_text = "\n".join(text_result)

        # ✅ Save transcription
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(full_text)

        if full_text.strip():
            print(f"✅ Transcription saved: {output_txt}")
            return output_txt
        else:
            print("⚠️ No speech recognized in the audio.")
            return None

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

    finally:
        if temp_wav and os.path.exists(temp_wav):  # ✅ Cleanup
            os.remove(temp_wav)
