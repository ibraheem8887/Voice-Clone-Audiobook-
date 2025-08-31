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
        
        # Try to read with wave to check if it's a valid WAV file
        with wave.open(audio_path, 'rb') as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)
            
            if duration == 0:
                return False, "Audio has 0 duration"
            
            return True, f"Valid audio file: {duration:.2f} seconds duration"
            
    except wave.Error:
        # Not a standard WAV file, try with pydub
        try:
            audio = AudioSegment.from_file(audio_path)
            duration = len(audio) / 1000.0  # Convert ms to seconds
            return True, f"Valid audio file: {duration:.2f} seconds duration"
        except Exception as e:
            return False, f"Invalid audio file: {str(e)}"
    except Exception as e:
        return False, f"Error checking audio file: {str(e)}"

def audio_to_text(input_audio, output_text="book_text.txt", minutes=5):
    """Simple audio to text converter for your voice cloning pipeline"""
    print("🔊 AUDIO TO TEXT CONVERTER")
    print("=" * 50)
    print(f"Input: {input_audio}")
    print(f"Output: {output_text}")
    print(f"Processing: First {minutes} minutes")
    print("=" * 50)
    
    # Check if file exists and is valid
    is_valid, message = check_audio_file(input_audio)
    if not is_valid:
        print(f"❌ {message}")
        return False
    
    print(f"✅ {message}")
    
    try:
        # Load audio file
        audio = AudioSegment.from_file(input_audio)
        duration_ms = len(audio)
        duration_min = duration_ms / 1000 / 60
        
        print(f"📊 Full audio duration: {duration_min:.1f} minutes")
        
        # Extract first X minutes
        process_ms = min(minutes * 60 * 1000, duration_ms)
        audio_segment = audio[:process_ms]
        
        # Export to WAV format for speech recognition
        temp_file = "temp_audio.wav"
        print("🔄 Preparing audio for speech recognition...")
        audio_segment.export(temp_file, format="wav")
        
        # Convert to text
        print("🎤 Converting audio to text...")
        recognizer = sr.Recognizer()
        
        with sr.AudioFile(temp_file) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
            
            try:
                text = recognizer.recognize_google(audio_data)
                print("✅ Speech recognition successful!")
            except sr.UnknownValueError:
                print("❌ Google Speech Recognition could not understand the audio")
                return False
            except sr.RequestError as e:
                print(f"❌ Could not request results from Google Speech Recognition service: {e}")
                return False
        
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        # Save text
        with open(output_text, "w", encoding="utf-8") as f:
            f.write(text)
        
        print(f"✅ Success! Extracted {len(text)} characters")
        print(f"💾 Text saved to: {output_text}")
        print(f"📝 Preview: {text[:150]}..." if len(text) > 150 else f"📝 Text: {text}")
        print("\n➡️  Next: Run 'true_voice_cloning.py' to convert text to YOUR VOICE!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        # Clean up temp file if it exists
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")
        return False

def list_audio_files():
    """List all audio files in current directory"""
    audio_extensions = ['.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg']
    audio_files = [f for f in os.listdir('.') 
                  if os.path.isfile(f) and any(f.lower().endswith(ext) for ext in audio_extensions)]
    
    return audio_files

if __name__ == "__main__":
    # List available audio files
    audio_files = list_audio_files()
    
    if not audio_files:
        print("❌ No audio files found in current directory.")
        print("Supported formats: .wav, .mp3, .m4a, .flac, .aac, .ogg")
    else:
        print("📁 Available audio files:")
        for i, file in enumerate(audio_files, 1):
            print(f"  {i}. {file}")
        
        # Try to use book_audio.wav if available, otherwise use first available file
        if "book_audio.wav" in audio_files:
            INPUT_AUDIO = "book_audio.wav"
        else:
            INPUT_AUDIO = audio_files[0]
            
        print(f"\nUsing: {INPUT_AUDIO}")
    
    # Configuration
    INPUT_AUDIO = "book_audio.wav"  # Your audio file
    OUTPUT_TEXT = "book_text.txt"   # Output text file
    
    # Process first 5 minutes (change as needed)
    success = audio_to_text(INPUT_AUDIO, OUTPUT_TEXT, minutes=5)
    
    if not success:
        print("\n🔧 Troubleshooting tips:")
        print("1. Check that your audio file is not corrupted")
        print("2. Ensure the audio has clear speech (not too much background noise)")
        print("3. Try a shorter audio segment (1-2 minutes)")
        print("4. Check your internet connection (Google Speech Recognition requires internet)")
        print("5. Try converting your audio to WAV format first")