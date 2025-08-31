import streamlit as st
import os
import subprocess
import sys
import shutil
import tempfile
from io import BytesIO

# Import your functions directly
sys.path.append('.')
from convert_to_aiVoice import text_to_speech_fast, read_text
from extract_pdf_text import extract_text

st.set_page_config(page_title="Voice Clone Audiobook Creator", page_icon="🎧")
st.title("🎧 Voice Clone Audiobook Creator")
st.write("Convert PDFs or audio files into audiobooks in your voice. Select a workflow and follow the steps.")

# ----------------------------
# Workflow selection
# ----------------------------
option = st.radio(
    "Select Workflow:",
    [
        "1️⃣ Convert PDF → AI Voice",
        "2️⃣ Convert PDF → Your Voice", 
        "3️⃣ Convert Audio → Your Voice",
        "4️⃣ Full Process (PDF → AI Voice → Your Voice)"
    ]
)

# ----------------------------
# Helper functions
# ----------------------------
def run_script(script_name, args=[]):
    """Run a script and ignore exit code"""
    cmd = [sys.executable, script_name] + args
    subprocess.run(cmd)

def cleanup_temp_files(files):
    """Remove temporary files"""
    for file in files:
        if os.path.exists(file):
            os.remove(file)

# ----------------------------
# File Upload
# ----------------------------
pdf_file, voice_file, audio_file = None, None, None

if option in ["1️⃣ Convert PDF → AI Voice", "2️⃣ Convert PDF → Your Voice", "4️⃣ Full Process (PDF → AI Voice → Your Voice)"]:
    pdf_file = st.file_uploader("Upload PDF", type="pdf")
    if pdf_file:
        with open("uploaded_book.pdf", "wb") as f:
            f.write(pdf_file.getbuffer())

if option in ["2️⃣ Convert PDF → Your Voice", "3️⃣ Convert Audio → Your Voice", "4️⃣ Full Process (PDF → AI Voice → Your Voice)"]:
    voice_file = st.file_uploader("Upload Voice Sample (WAV)", type="wav")
    if voice_file:
        os.makedirs("myVoice", exist_ok=True)
        with open("myVoice/myVoice.wav", "wb") as f:
            f.write(voice_file.getbuffer())

if option == "3️⃣ Convert Audio → Your Voice":
    audio_file = st.file_uploader("Upload Audio File (WAV/MP3)", type=["wav","mp3"])
    if audio_file:
        with open("input_audio.wav", "wb") as f:
            f.write(audio_file.getbuffer())

# ----------------------------
# Run Workflow
# ----------------------------
if st.button("Start Workflow"):
    try:
        temp_files_to_cleanup = []
        
        # -------- PDF → AI Voice --------
        if option in ["1️⃣ Convert PDF → AI Voice", "4️⃣ Full Process (PDF → AI Voice → Your Voice)"] and pdf_file:
            if not os.path.exists("book_text.txt"):
                # Use direct function call instead of subprocess
                extract_text("uploaded_book.pdf", "book_text.txt")
            
            if os.path.exists("book_text.txt"):
                # Use direct function call instead of subprocess
                try:
                    full_text = read_text("book_text.txt")
                    # Generate audio and get bytes
                    text_to_speech_fast(full_text, "/tmp/book_audio.mp3")
                    
                    st.success("✅ AI voice conversion completed!")
                    
                    # Play audio directly from /tmp/
                    with open("/tmp/book_audio.mp3", "rb") as f:
                        audio_bytes = f.read()
                    
                    st.audio(audio_bytes, format="audio/mp3")
                    
                    # Download button
                    st.download_button(
                        "Download AI Voice Audiobook",
                        audio_bytes,
                        "ai_voice_audiobook.mp3",
                        "audio/mp3"
                    )
                    
                    temp_files_to_cleanup.append("/tmp/book_audio.mp3")
                    
                except Exception as e:
                    st.error(f"Audio generation failed: {e}")

        # -------- PDF → Your Voice --------
        if option in ["2️⃣ Convert PDF → Your Voice", "4️⃣ Full Process (PDF → AI Voice → Your Voice)"] and pdf_file and voice_file:
            if not os.path.exists("book_text.txt"):
                run_script("extract_pdf_text.py", ["uploaded_book.pdf", "book_text.txt"])
            if os.path.exists("book_text.txt"):
                run_script("convert_to_myVoice.py")
                run_script("merge_audio.py")
                if os.path.exists("/tmp/my_voice_audiobook.wav"):
                    st.success("✅ Your voice audiobook completed!")
                    with open("/tmp/my_voice_audiobook.wav", "rb") as f:
                        audio_data = f.read()
                    st.audio(audio_data, format="audio/wav")
                    st.download_button(
                        "Download Your Voice Audiobook",
                        audio_data,
                        "my_voice_audiobook.wav",
                        "audio/wav"
                    )
                    temp_files_to_cleanup.append("/tmp/my_voice_audiobook.wav")

        # -------- Audio → Your Voice --------
        if option == "3️⃣ Convert Audio → Your Voice" and audio_file and voice_file:
            run_script("audio_to_text.py", ["input_audio.wav"])
            run_script("convert_to_myVoice.py")
            run_script("merge_audio.py")
            if os.path.exists("/tmp/my_voice_audiobook.wav"):
                st.success("✅ Your voice audiobook completed!")
                with open("/tmp/my_voice_audiobook.wav", "rb") as f:
                    audio_data = f.read()
                st.audio(audio_data, format="audio/wav")
                st.download_button(
                    "Download Your Voice Audiobook",
                    audio_data,
                    "my_voice_audiobook.wav",
                    "audio/wav"
                )
                temp_files_to_cleanup.append("/tmp/my_voice_audiobook.wav")

        # Clean temporary input files
        temp_files_to_cleanup.extend(["uploaded_book.pdf", "input_audio.wav"])
        cleanup_temp_files(temp_files_to_cleanup)

    except Exception as e:
        st.error(f"Workflow failed: {str(e)}")

# ----------------------------
# Start Over
# ----------------------------
if st.button("Start Over"):
    cleanup_temp_files([
        "uploaded_book.pdf", "book_text.txt", 
        "/tmp/book_audio.mp3", "/tmp/my_voice_audiobook.wav", 
        "input_audio.wav"
    ])
    st.rerun()
