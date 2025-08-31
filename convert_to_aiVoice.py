import os
import sys
import tempfile
from gtts import gTTS
sys.stdout.reconfigure(encoding='utf-8')

TEXT_FILE = "book_text.txt"

def read_text(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found!")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def text_to_speech_fast(text):
    print("🔊 Starting audiobook conversion with gTTS...")
    
    try:
        start_time = time.time()
        
        # Use gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tts.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        elapsed = time.time() - start_time
        
        # Read the audio data
        with open(tmp_path, "rb") as f:
            audio_data = f.read()
        
        # Clean up
        os.unlink(tmp_path)
        
        print(f"✅ Audiobook completed in {int(elapsed)} seconds")
        return audio_data
        
    except Exception as e:
        print(f"❌ Audio generation failed: {e}")
        return None

if __name__ == "__main__":
    full_text = read_text(TEXT_FILE)
    audio_data = text_to_speech_fast(full_text)
    
    if audio_data:
        # Save to /tmp/ for other scripts
        with open("/tmp/book_audio.mp3", "wb") as f:
            f.write(audio_data)
        print("✅ Audio saved to /tmp/book_audio.mp3")
    else:
        print("❌ Failed to generate audio")
        sys.exit(1)
