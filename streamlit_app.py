import streamlit as st
import os
import io
import sys
import tempfile
from pyttsx3_audiobook_fast import text_to_speech_fast, read_text
from voice_cloning_fixed import true_voice_cloning
from merge_audio_chunks_memory import merge_audio_chunks_memory

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
# File Upload
# ----------------------------
pdf_file = voice_file = audio_file = None

if option in ["1️⃣ Convert PDF → AI Voice", "2️⃣ Convert PDF → Your Voice", "4️⃣ Full Process (PDF → AI Voice → Your Voice)"]:
    pdf_file = st.file_uploader("Upload PDF", type="pdf")

if option in ["2️⃣ Convert PDF → Your Voice", "3️⃣ Convert Audio → Your Voice", "4️⃣ Full Process (PDF → AI Voice → Your Voice)"]:
    voice_file = st.file_uploader("Upload Voice Sample (WAV)", type="wav")

if option == "3️⃣ Convert Audio → Your Voice":
    audio_file = st.file_uploader("Upload Audio File (WAV/MP3)", type=["wav","mp3"])

# ----------------------------
# Run Workflow
# ----------------------------
if st.button("Start Workflow"):
    try:
        # Temporary directory for session files
        TMP_DIR = tempfile.mkdtemp()
        book_text_path = os.path.join(TMP_DIR, "book_text.txt")

        # -------- PDF → AI Voice --------
        if option in ["1️⃣ Convert PDF → AI Voice", "4️⃣ Full Process (PDF → AI Voice → Your Voice)"] and pdf_file:
            pdf_bytes = pdf_file.read()
            pdf_path = os.path.join(TMP_DIR, "uploaded_book.pdf")
            with open(pdf_path, "wb") as f:
                f.write(pdf_bytes)

            # Extract text
            from extract_pdf_text import extract_text
            extract_text(pdf_path, book_text_path)

            # AI Voice conversion
            full_text = read_text(book_text_path)
            ai_audio_path = os.path.join(TMP_DIR, "book_audio.mp3")
            text_to_speech_fast(full_text, ai_audio_path)

            st.success("✅ AI voice conversion completed!")
            st.audio(ai_audio_path)
            with open(ai_audio_path, "rb") as f:
                st.download_button("Download AI Voice Audiobook", f, "ai_voice_audiobook.mp3", "audio/mp3")

        # -------- PDF → Your Voice --------
        if option in ["2️⃣ Convert PDF → Your Voice", "4️⃣ Full Process (PDF → AI Voice → Your Voice)"] and pdf_file and voice_file:
            # Save voice sample
            voice_path = os.path.join(TMP_DIR, "myVoice.wav")
            os.makedirs(os.path.dirname(voice_path), exist_ok=True)
            with open(voice_path, "wb") as f:
                f.write(voice_file.read())

            # Generate voice chunks
            chunks_bytes_list = true_voice_cloning(text_file=book_text_path, voice_file=voice_path)

            if chunks_bytes_list:
                merged_audio = merge_audio_chunks_memory(chunks_bytes_list, output_file=os.path.join(TMP_DIR,"my_voice_audiobook.wav"), export_format="wav", save_to_disk=True)
                st.success("✅ Your voice audiobook completed!")
                st.audio(merged_audio, format="audio/wav")
                merged_audio.seek(0)
                st.download_button("Download Your Voice Audiobook", merged_audio, "my_voice_audiobook.wav", "audio/wav")

        # -------- Audio → Your Voice --------
        if option == "3️⃣ Convert Audio → Your Voice" and audio_file and voice_file:
            # TODO: integrate audio_to_text function here if available
            st.warning("Audio → Your Voice workflow not fully implemented in cloud-ready version")

    except Exception as e:
        st.error(f"Workflow failed: {str(e)}")

# ----------------------------
# Start Over
# ----------------------------
if st.button("Start Over"):
    st.experimental_rerun()
