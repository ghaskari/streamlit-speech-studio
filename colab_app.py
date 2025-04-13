import gradio as gr
import subprocess
import os
import tempfile
import speech_recognition as sr
import asyncio
import edge_tts

# Language codes compatible with edge-tts (Voice mappings)
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

def convert_mp3_to_wav(mp3_file):
    temp_dir = tempfile.mkdtemp()
    wav_path = os.path.join(temp_dir, "converted.wav")
    try:
        subprocess.run(["ffmpeg", "-i", mp3_file.name, "-ar", "16000", "-ac", "1", wav_path],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return wav_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg conversion failed: {e.stderr.decode()}")

def transcribe_audio(mp3_file, language_code):
    try:
        wav_path = convert_mp3_to_wav(mp3_file)
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language=language_code)

        temp_dir = tempfile.mkdtemp()
        txt_path = os.path.join(temp_dir, "transcription.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        return text, txt_path
    except FileNotFoundError:
        return "Error: File not found.", None
    except sr.UnknownValueError:
        return "Error: Speech could not be understood.", None
    except sr.RequestError as e:
        return f"Error: Could not request results; {e}", None
    except Exception as e:
        return f"Unexpected error: {e}", None

def text_to_speech(text, voice_name):
    try:
        temp_dir = tempfile.mkdtemp()
        mp3_path = os.path.join(temp_dir, "output.mp3")

        async def generate():
            communicate = edge_tts.Communicate(text=text, voice=voice_name)
            await communicate.save(mp3_path)

        asyncio.run(generate())
        return mp3_path, mp3_path
    except Exception as e:
        return f"Error generating TTS: {e}", None

with gr.Blocks(title="🎙️ MP3 Transcriber + Text to Speech") as demo:
    gr.Markdown("## 🎙️ Transcription + High-Quality TTS using `edge-tts`")

    with gr.Tab("🗣️ Transcribe Audio"):
        gr.Markdown("Upload an MP3 file and choose the language.")
        with gr.Row():
            audio_input = gr.File(label="Upload MP3", file_types=[".mp3"])
            lang_dropdown = gr.Dropdown(
                choices=list(VOICE_MAP.keys()),
                value="🇮🇷 Persian (fa)",
                label="Language",
                interactive=True
            )
        with gr.Row():
            output_text = gr.Textbox(label="Transcription", lines=10)
            download_file = gr.File(label="Download .txt")
        transcribe_button = gr.Button("Transcribe")

    with gr.Tab("🔊 Text to Speech"):
        gr.Markdown("Enter text and get downloadable MP3.")
        with gr.Row():
            tts_input = gr.Textbox(label="Text Input", lines=5)
            tts_lang_dropdown = gr.Dropdown(
                choices=list(VOICE_MAP.keys()),
                value="🇮🇷 Persian (fa)",
                label="Language",
                interactive=True
            )
        with gr.Row():
            tts_audio = gr.Audio(label="Speech Output", type="filepath")
            tts_download = gr.File(label="Download MP3")
        tts_button = gr.Button("Generate MP3")

    transcribe_button.click(
        fn=lambda file, lang: transcribe_audio(file, VOICE_MAP[lang].split("-")[0] + "-" + VOICE_MAP[lang].split("-")[1]),
        inputs=[audio_input, lang_dropdown],
        outputs=[output_text, download_file]
    )

    tts_button.click(
        fn=lambda text, lang: text_to_speech(text, VOICE_MAP[lang]),
        inputs=[tts_input, tts_lang_dropdown],
        outputs=[tts_audio, tts_download]
    )

demo.launch()
