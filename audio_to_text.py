# audio_to_text.py
import speech_recognition as sr
from pydub import AudioSegment
import os
import wave

def check_audio_file(audio_path):
    """Check if audio file is valid and readable"""
    if not os.path.exists(audio_path):
        return False, f"File {audio_path} does not exist"
    
    try:
        # Try to read basic file info
        file_size = os.path.getsize(audio_path)
        if file_size == 0:
            return False, "File is empty (0 bytes)"
        
        # Try with wave (works for WAV files)
        with wave.open(audio_path, 'rb') as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)
            if duration == 0:
                return False, "Audio has 0 duration"
            return True, f"Valid audio file: {duration:.2f} seconds duration"
    except wave.Error:
        # Not a plain WAV → fallback to pydub
        try:
            audio = AudioSegment.from_file(audio_path)
            duration = len(audio) / 1000.0
            return True, f"Valid audio file: {duration:.2f} seconds duration"
        except Exception as e:
            return False, f"Invalid audio file: {str(e)}"
    except Exception as e:
        return False, f"Error checking audio file: {str(e)}"

def audio_to_text(input_audio, output_text="book_text.txt", minutes=5):
    """Convert speech in audio to text (for Your Voice workflow)"""
    print("🔊 AUDIO → TEXT")
    print("=" * 50)
    print(f"Input : {input_audio}")
    print(f"Output: {output_text}")
    
    # Check audio
    is_valid, message = check_audio_file(input_audio)
    if not is_valid:
        print(f"❌ {message}")
        return False
    print(f"✅ {message}")

    try:
        # Load audio
        audio = AudioSegment.from_file(input_audio)
        process_ms = min(minutes * 60 * 1000, len(audio))
        audio_segment = audio[:process_ms]

        # Export as wav for recognition
        temp_file = "temp_audio.wav"
        audio_segment.export(temp_file, format="wav")

        # Recognize
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_file) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio_data = recognizer.record(source)

            try:
                text = recognizer.recognize_google(audio_data, language="en-US")
                print("✅ Speech recognition successful!")
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
                return False
            except sr.RequestError as e:
                print(f"❌ API error: {e}")
                return False

        os.remove(temp_file)

        # Save text
        with open(output_text, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"💾 Text saved to {output_text}")
        print(f"📝 Preview: {text[:120]}...")
        return True

    except Exception as e:
        print(f"❌ Processing error: {e}")
        return False

if __name__ == "__main__":
    # Auto-pick audio file
    audio_files = [f for f in os.listdir('.') if f.lower().endswith(('.wav', '.mp3', '.m4a'))]
    if not audio_files:
        print("❌ No audio files found.")
    else:
        input_audio = audio_files[0]  # pick first available
        output_text = "book_text.txt"
        audio_to_text(input_audio, output_text, minutes=5)
