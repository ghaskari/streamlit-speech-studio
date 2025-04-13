# 🎙️ streamlit-speech-studio

Multilingual MP3 Transcription + Text-to-Speech Tool
Built with **Streamlit** for local use and **Gradio** for Google Colab compatibility.

---

## 🧠 Model 1: `streamlit_app.py` — Local Desktop Interface

### ✅ Purpose

Designed to be run **locally** on a personal machine with a graphical user interface (GUI) powered by **Streamlit**.

### 🧩 Components

- **UI Library**: [streamlit](https://streamlit.io/)
- **Speech Recognition**: `speechrecognition` (Google API)
- **TTS Engine**: `edge-tts` (Microsoft neural voices)
- **File Conversion**: `ffmpeg` (for `.mp3` → `.wav`)

### 🖼️ UI Features

- **Tab 1: Transcription**
    - Upload `.mp3` file
    - Choose language
    - Transcribe using Google’s speech recognition
    - Display transcription + download `.txt`
- **Tab 2: Text-to-Speech**
    - Input custom text
    - Choose voice (e.g. Persian, Arabic, English)
    - Generate `.mp3` using `edge-tts`
    - Playback audio + download file

### ⚙️ How It Runs

```bash
streamlit run app/streamlit_app.py
```

---

### 💻 Ideal For

- Offline/local desktop use
- Developers or linguists working on audio content
- No need to upload files online

---

## 🌐 Model 2: `colab_app.py` — Colab-based Gradio Interface

### ✅ Purpose

Designed to run **in the browser via Google Colab**, using **Gradio** to provide a simple, clean UI.

### 🧩 Components

- **UI Library**: [gradio](https://www.gradio.app/)
- **Speech Recognition**: `speechrecognition` (Google API)
- **TTS Engine**: `edge-tts`
- **File Conversion**: `ffmpeg` (installed in Colab with `apt`)

### 🖼️ UI Features

- **Transcribe Tab**
    - Upload `.mp3`
    - Choose language
    - Transcribe using Google’s speech API
    - Output + `.txt` download
- **TTS Tab**
    - Input text
    - Select voice/language
    - Generate `.mp3` with neural voice
    - Listen + download audio

### ⚙️ How to Run in Colab

1. Upload or open `colab_app.py` in Google Colab.
2. Install dependencies:
    
    ```bash
    !pip install gradio speechrecognition edge-tts
    !apt install ffmpeg
    
    ```
    
3. Run the app:
    
    ```bash
    !python colab_app.py
    
    ```
    

### 🌍 Ideal For

- Quick demos or sharing
- No local setup required
- Cross-platform access (runs in any browser)

---

## 🆚 Summary Comparison

| Feature | `streamlit_app.py` | `colab_app.py` |
| --- | --- | --- |
| Interface | Streamlit | Gradio |
| Platform | Local/Desktop | Google Colab (Web) |
| Input Files | `.mp3` | `.mp3` |
| Output Formats | `.txt`, `.mp3` | `.txt`, `.mp3` |
| TTS Engine | `edge-tts` (MS voices) | `edge-tts` |
| Audio Playback | Native audio player | Gradio audio widget |
| Download Support | ✅ | ✅ |
| Best For | Local workflows | Cloud/web demos |

---