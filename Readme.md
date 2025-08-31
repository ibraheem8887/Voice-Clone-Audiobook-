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
git clone https://github.com/ibraheem8887/voice-clone-audiobook-.git
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

