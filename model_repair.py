# File: force_model_download.py
import os
import shutil
import requests
import zipfile
import tempfile
from TTS.api import TTS

def force_download_models():
    print("🔄 FORCING MODEL DOWNLOAD...")
    
    # Clear ALL TTS cache directories
    cache_paths = [
        os.path.expanduser("~/.local/share/tts"),
        os.path.expanduser("~/AppData/Local/tts"), 
        os.path.expanduser("~/.cache/tts"),
        os.path.join(os.getcwd(), "tts_cache")
    ]
    
    for cache_path in cache_paths:
        if os.path.exists(cache_path):
            print(f"🗑️ Deleting: {cache_path}")
            shutil.rmtree(cache_path, ignore_errors=True)
    
    # Set custom cache directory in current folder
    custom_cache = os.path.join(os.getcwd(), "tts_models")
    os.makedirs(custom_cache, exist_ok=True)
    os.environ["TTS_HOME"] = custom_cache
    
    print(f"📁 Using cache: {custom_cache}")
    
    try:
        print("📥 Downloading YourTTS model (this will take 15-30 minutes)...")
        
        # This should force a fresh download
        tts = TTS("tts_models/multilingual/multi-dataset/your_tts", gpu=False)
        
        print("✅ Model downloaded successfully!")
        
        # Test it
        print("🧪 Testing voice cloning...")
        tts.tts_to_file(
            text="This is a test of voice cloning with my voice.",
            speaker_wav="myVoice/myVoice.wav",
            language="en", 
            file_path="voice_test.wav"
        )
        print("✅ Test successful! Ready for full conversion.")
        
        return True
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

if __name__ == "__main__":
    force_download_models()