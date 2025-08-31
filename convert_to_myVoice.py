# File: voice_cloning_fixed.py
import os
import sys


# Force UTF-8 encoding for prints
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')
import time
import shutil
from TTS.api import TTS


def true_voice_cloning():
    # Configuration
    INPUT_TEXT = "book_text.txt"
    VOICE_FILE = "myVoice/myVoice.wav"
    AUDIO_DIR = "audio_chunks"
    CHUNK_SIZE = 400
    
    print("🎯 VOICE CLONING WITH YOUR VOICE")
    print("=" * 50)
    
    # Verify files exist
    if not os.path.exists(INPUT_TEXT):
        print(f"❌ Error: {INPUT_TEXT} not found!")
        return False
        
    if not os.path.exists(VOICE_FILE):
        print(f"❌ Error: {VOICE_FILE} not found!")
        return False
    
    # Create output directory
    os.makedirs(AUDIO_DIR, exist_ok=True)
    
    # Read text file
    try:
        with open(INPUT_TEXT, 'r', encoding='utf-8') as f:
            full_text = f.read()
        print(f"📖 Read {len(full_text)} characters")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Split text into chunks
    words = full_text.split()
    chunks = []
    for i in range(0, len(words), CHUNK_SIZE):
        chunk_text = ' '.join(words[i:i+CHUNK_SIZE])
        chunks.append(chunk_text)
    
    print(f"✂️  Split into {len(chunks)} chunks")
    
    # Initialize TTS - try multiple approaches
    try:
        print("🔊 Downloading YourTTS model (this will take a while)...")
        
        # First, ensure any corrupted files are gone
        model_path = os.path.expanduser("~/.local/share/tts/tts_models--multilingual--multi-dataset--your_tts")
        if os.path.exists(model_path):
            shutil.rmtree(model_path)
            print("🧹 Cleared old model files")
        
        # Now download fresh
        tts = TTS("tts_models/multilingual/multi-dataset/your_tts", gpu=False)
        print("✅ YourTTS model loaded successfully!")
        
    except Exception as e:
        print(f"❌ Failed to load YourTTS: {e}")
        print("🔄 Trying alternative approach...")
        return False
    
    # Test with small sample
    try:
        print("🧪 Testing voice cloning...")
        tts.tts_to_file(
            text="This is a voice cloning test with my voice.",
            speaker_wav=VOICE_FILE,
            language="en",
            file_path="test_my_voice.wav"
        )
        print("✅ Voice test successful! Sounds like YOU!")
    except Exception as e:
        print(f"❌ Voice test failed: {e}")
        return False
    
    # Process all chunks
    print(f"\n🎵 Creating {len(chunks)} chunks with YOUR voice...")
    successful_chunks = 0
    
    for i, chunk in enumerate(chunks):
        output_path = os.path.join(AUDIO_DIR, f"chunk_{i}.mp3")
        
        print(f"[{i+1}/{len(chunks)}] Processing...")
        
        try:
            tts.tts_to_file(
                text=chunk,
                speaker_wav=VOICE_FILE,
                language="en",
                file_path=output_path
            )
            successful_chunks += 1
            print(f"✅ Saved: chunk_{i}.mp3")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Failed chunk {i+1}: {e}")
            continue
    
    # Results
    print(f"\n{'='*50}")
    if successful_chunks > 0:
        print(f"🎉 Created {successful_chunks} chunks with YOUR VOICE!")
        print(f"📁 Files in: {AUDIO_DIR}/")
        print(f"➡️  Run: python merge_audio.py")
        return True
    else:
        print("❌ No chunks created")
        return False

if __name__ == "__main__":
    true_voice_cloning()