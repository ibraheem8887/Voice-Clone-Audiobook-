# 🎧 Voice Clone Audiobook Creator

Convert **PDFs or audio files into audiobooks** with **AI voices** or **your cloned voice**.

---

## ✨ Features

- 📖 **Extract text from PDFs** – Convert PDF documents to readable text  
- 🎤 **Transcribe audio** – Use Google Speech Recognition to convert audio to text  
- 🤖 **Generate AI voices** – Create audiobooks with synthetic AI narration  
- 👤 **Clone your voice** – Personalize narration with your own cloned voice  
- 🔗 **Merge audio chunks** – Combine segmented audio into complete audiobooks  
- 🌐 **Web interface** – User-friendly Streamlit-based application  
- ⚡ **Multiple workflows** – Support for various input/output combinations  

---

## 🚀 Quick Start

### Prerequisites
- Python **3.7+**  
- **FFmpeg** installed on your system  
- Internet connection (for speech recognition and model downloading)  

### Installation
Clone the repository:

```bash
git clone https://github.com/your-username/voice-clone-audiobook-creator.git
cd voice-clone-audiobook-creator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install **FFmpeg**:  
- **Windows** → [ffmpeg.org](https://ffmpeg.org)  
- **macOS** → `brew install ffmpeg`  
- **Linux** → `sudo apt install ffmpeg`  

---

## ▶️ Usage

### Web Interface (Recommended)
```bash
streamlit run streamlit_app.py
```
Then open in your browser → [http://localhost:8501](http://localhost:8501)  

### Command Line
```bash
# Extract text from PDF
python extract_pdf_text.py  

# Transcribe audio to text
python audio_to_text.py  

# Generate AI voice audiobook
python convert_to_aiVoice.py  

# Create voice-cloned audiobook
python convert_to_myVoice.py
python merge_audio.py  

# Fix model download issues
python model_repair.py
```

---

## 📋 Workflows

1. **PDF → AI Voice** – Convert PDF documents to AI-narrated audiobooks  
2. **PDF → Your Voice** – Create audiobooks narrated in your cloned voice  
3. **Audio → Your Voice** – Convert existing audio into your voice  
4. **PDF → AI Voice → Your Voice** – Generate both AI and custom voice versions  

---

## 📁 Project Structure

```text
voice-clone-audiobook-creator/
├── streamlit_app.py          # Main web interface
├── extract_pdf_text.py       # PDF text extraction
├── audio_to_text.py          # Audio transcription
├── convert_to_aiVoice.py     # AI voice generation
├── convert_to_myVoice.py     # Voice cloning module
├── merge_audio.py            # Audio chunk merging
├── model_repair.py           # Model download utility
├── myVoice/                  # Voice samples directory
│   └── myVoice.wav           # Your voice sample
├── audio_chunks/             # Generated audio chunks
├── book_text.txt             # Extracted text
├── book_audio.mp3            # AI-generated audiobook
├── my_voice_audiobook.wav    # Voice-cloned audiobook
└── requirements.txt          # Python dependencies
```

---

## 🔧 Troubleshooting

### Common Issues

- **Model download issues**  
```bash
python model_repair.py
```

- **Audio processing errors**  
  - Ensure FFmpeg is installed and in your PATH  
  - Verify audio file integrity  

- **Memory errors**  
  - Reduce `CHUNK_SIZE` in `convert_to_myVoice.py`  
  - Process smaller documents  

- **Voice cloning quality**  
  - Use a high-quality, clear voice sample (1–2 minutes of speech)  
  - Minimize background noise  

- **Speech recognition failures**  
  - Check internet connection  
  - Ensure audio has clear speech with minimal noise  

### Performance Tips
- ⚡ Use AI voice generation for faster processing  
- 🖥️ Use a GPU for faster voice cloning  
- 📖 Split large documents into smaller sections  

---

## 📊 Sample Processing Times

| Document Size | AI Voice | Your Voice |
|---------------|----------|------------|
| 10 pages      | ~1 min   | ~15–30 min |
| 50 pages      | ~5 min   | ~60–90 min |
| 100 pages     | ~10 min  | ~2–3 hours |

> ⏱️ *Note: Voice cloning time depends heavily on your hardware*  

---

## 🤝 Contributing

1. Fork the project  
2. Create your feature branch → `git checkout -b feature/AmazingFeature`  
3. Commit your changes → `git commit -m 'Add some AmazingFeature'`  
4. Push to branch → `git push origin feature/AmazingFeature`  
5. Open a Pull Request  

---

## 📝 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.  

---

## 🙏 Acknowledgments

- [Coqui AI](https://github.com/coqui-ai/TTS) – TTS library & voice cloning  
- Google Speech Recognition API  
- Streamlit framework  
- All contributors & open-source libraries  

---

## 📞 Support

If you encounter any issues:  
- Check the **Troubleshooting** section above  
- Review code comments in each module  
- Open an issue on the GitHub repository  

> ⚠️ **Note**: This software is for personal use only. Ensure you have the rights to any content you process.

