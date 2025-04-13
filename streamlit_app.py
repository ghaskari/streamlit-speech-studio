import streamlit as st
import tempfile
import os
import subprocess
import speech_recognition as sr
import asyncio
import edge_tts

# --- Voice Mapping ---
VOICE_MAP = {
    "🇮🇷 Persian (fa)": "fa-IR-DilaraNeural",
    "🇺🇸 English (en)": "en-US-JennyNeural",
    "🇸🇦 Arabic (ar)": "ar-EG-SalmaNeural",
    "🇫🇷 French (fr)": "fr-FR-DeniseNeural",
    "🇩🇪 German (de)": "de-DE-KatjaNeural",
    "🇪🇸 Spanish (es)": "es-ES-ElviraNeural",
    "🇹🇷 Turkish (tr)": "tr-TR-AhmetNeural",
    "🇮🇳 Hindi (hi)": "hi-IN-SwaraNeural"
}

def extract_lang_code(voice_name):
    return "-".join(voice_name.split("-")[:2])

def convert_mp3_to_wav(mp3_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as mp3_file:
        mp3_file.write(mp3_bytes)
        mp3_path = mp3_file.name

    wav_path = mp3_path.replace(".mp3", ".wav")
    subprocess.run(["ffmpeg", "-y", "-i", mp3_path, "-ar", "16000", "-ac", "1", wav_path],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return wav_path

def transcribe_audio(audio_bytes, lang_code):
    wav_path = convert_mp3_to_wav(audio_bytes)

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)

    text = recognizer.recognize_google(audio, language=lang_code)
    return text

def text_to_speech(text, voice_name):
    temp_dir = tempfile.mkdtemp()
    mp3_path = os.path.join(temp_dir, "tts_output.mp3")

    async def generate():
        communicate = edge_tts.Communicate(text=text, voice=voice_name)
        await communicate.save(mp3_path)

    asyncio.run(generate())
    return mp3_path

# --- Streamlit UI ---
st.set_page_config(page_title="🗣️ TTS & Transcriber", layout="centered")
st.title("🎙️ Multilingual Transcriber & Text-to-Speech")

tab1, tab2 = st.tabs(["🗣️ Transcribe Audio", "🔊 Text to Speech"])

# --- Transcription Tab ---
with tab1:
    st.header("Transcribe MP3 File")
    lang_display = st.selectbox("Choose Language", list(VOICE_MAP.keys()), index=0)
    uploaded_file = st.file_uploader("Upload an MP3 file", type=["mp3"])

    if uploaded_file:
        try:
            lang_code = extract_lang_code(VOICE_MAP[lang_display])
            with st.spinner("Transcribing..."):
                text = transcribe_audio(uploaded_file.read(), lang_code)

            st.text_area("Transcription Result", value=text, height=150)

            st.download_button("📄 Download Transcription", text.encode("utf-8"),
                               file_name="transcription.txt", mime="text/plain")

        except Exception as e:
            st.error(f"❌ Error during transcription: {e}")

# --- TTS Tab ---
with tab2:
    st.header("Generate Speech from Text")
    input_text = st.text_area("Enter Text to Convert", height=150)
    tts_lang = st.selectbox("Choose Voice", list(VOICE_MAP.keys()), index=0)

    if st.button("🎤 Generate Speech") and input_text.strip():
        try:
            with st.spinner("Generating MP3..."):
                mp3_path = text_to_speech(input_text, VOICE_MAP[tts_lang])

            st.audio(mp3_path, format="audio/mp3")
            with open(mp3_path, "rb") as f:
                st.download_button("📥 Download MP3", f, file_name="output.mp3", mime="audio/mpeg")

        except Exception as e:
            st.error(f"❌ Error during TTS: {e}")
