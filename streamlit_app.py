import streamlit as st
import tempfile
import os
import subprocess
import speech_recognition as sr
import asyncio
import edge_tts

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

def save_uploaded_file(uploaded_file):
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        return tmp_file.name

def convert_to_pcm_wav(input_path):
    wav_path = os.path.splitext(input_path)[0] + "_converted.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-ac", "1", "-ar", "16000", "-f", "wav", wav_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return wav_path

def transcribe_audio(file_path, lang_code):
    pcm_wav_path = convert_to_pcm_wav(file_path)
    recognizer = sr.Recognizer()
    with sr.AudioFile(pcm_wav_path) as source:
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
    st.header("Transcribe Audio File")
    lang_display = st.selectbox("Choose Language", list(VOICE_MAP.keys()), index=0)
    uploaded_file = st.file_uploader("Upload an MP3 or WAV file", type=["mp3", "wav"])

    if uploaded_file:
        lang_code = extract_lang_code(VOICE_MAP[lang_display])
        file_path = save_uploaded_file(uploaded_file)

        if st.button("🎙️ Start Transcription"):
            with st.spinner("Transcribing..."):
                text = transcribe_audio(file_path, lang_code)
                st.session_state['transcription_text'] = text

    # Show result if exists
    if 'transcription_text' in st.session_state:
        st.text_area("Transcription Result", value=st.session_state['transcription_text'], height=150)
        st.download_button("📄 Download Transcription",
                           st.session_state['transcription_text'].encode("utf-8"),
                           file_name="transcription.txt", mime="text/plain")

# --- TTS Tab ---
with tab2:
    st.header("Generate Speech from Text")
    input_text = st.text_area("Enter Text to Convert", height=150)
    tts_lang = st.selectbox("Choose Voice", list(VOICE_MAP.keys()), index=0)

    if st.button("🎤 Generate Speech") and input_text.strip():
        with st.spinner("Generating MP3..."):
            mp3_path = text_to_speech(input_text, VOICE_MAP[tts_lang])
            st.session_state['tts_file'] = mp3_path

    # Play and download if exists
    if 'tts_file' in st.session_state and os.path.exists(st.session_state['tts_file']):
        st.audio(st.session_state['tts_file'], format="audio/mp3")
        with open(st.session_state['tts_file'], "rb") as f:
            st.download_button("📥 Download MP3", f,
                               file_name="output.mp3", mime="audio/mpeg")
