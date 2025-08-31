import os
import sys
import time
import shutil

# Force UTF-8 encoding for prints
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

def true_voice_cloning():
    # Configuration - REDUCED chunk size for cloud compatibility
    INPUT_TEXT = "book_text.txt"
    VOICE_FILE = "myVoice/myVoice.wav"
    AUDIO_DIR = "audio_chunks"
    CHUNK_SIZE = 150  # Reduced from 400 for cloud stability
    
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
    
    # Split text into chunks (smaller for cloud stability)
    words = full_text.split()
    chunks = []
    for i in range(0, len(words), CHUNK_SIZE):
        chunk_text = ' '.join(words[i:i+CHUNK_SIZE])
        chunks.append(chunk_text)
    
    print(f"✂️  Split into {len(chunks)} chunks")
    
    # Initialize TTS with better error handling
    try:
        print("🔊 Downloading YourTTS model (this will take a while)...")
        
        # Clear cache - use a more robust approach
        cache_paths = [
            os.path.expanduser("~/.local/share/tts"),
            os.path.expanduser("~/.cache/tts"),
            os.path.join(os.getcwd(), "tts_cache")
        ]
        
        for cache_path in cache_paths:
            if os.path.exists(cache_path):
                shutil.rmtree(cache_path, ignore_errors=True)
                print(f"🧹 Cleared: {cache_path}")
        
        # Set custom cache directory
        custom_cache = os.path.join(os.getcwd(), "tts_models")
        os.makedirs(custom_cache, exist_ok=True)
        os.environ["TTS_HOME"] = custom_cache
        
        # Now download fresh with progress indication
        tts = TTS("tts_models/multilingual/multi-dataset/your_tts", 
                 progress_bar=True, gpu=False)
        print("✅ YourTTS model loaded successfully!")
        
    except Exception as e:
        print(f"❌ Failed to load YourTTS: {e}")
        print("💡 This is likely a Python version issue.")
        print("   TTS requires Python 3.9-3.11, but this environment uses Python 3.13.6")
        print("   Add a 'runtime.txt' file with: python-3.11.9")
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
    
    # Process all chunks with better error handling
    print(f"\n🎵 Creating {len(chunks)} chunks with YOUR voice...")
    successful_chunks = 0
    
    for i, chunk in enumerate(chunks):
        output_path = os.path.join(AUDIO_DIR, f"chunk_{i}.wav")  # Changed to WAV for consistency
        
        print(f"[{i+1}/{len(chunks)}] Processing {len(chunk)} characters...")
        
        try:
            # Skip empty chunks
            if not chunk.strip():
                print(f"⚠️  Skipping empty chunk {i+1}")
                continue
                
            tts.tts_to_file(
                text=chunk,
                speaker_wav=VOICE_FILE,
                language="en",
                file_path=output_path
            )
            successful_chunks += 1
            print(f"✅ Saved: chunk_{i}.wav")
            
            # Smaller delay for cloud environment
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Failed chunk {i+1}: {e}")
            # Try to continue with next chunk
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
        print("💡 This is likely due to Python version incompatibility")
        print("   TTS requires Python 3.9-3.11, but this is Python 3.13.6")
        print("   Add a 'runtime.txt' file with: python-3.11.9")
        return False

if __name__ == "__main__":
    true_voice_cloning()
