import streamlit as st
import openai
from gtts import gTTS
import tempfile
import os

# ------------------- SETUP -------------------
st.set_page_config(page_title="Speech ↔ Text App", layout="centered")
st.title("🎙️ Text-to-Speech & Speech-to-Text App")

# 🔑 Get API key securely from Streamlit Secrets
# In Streamlit Cloud, add your key in Settings → Secrets → Add:
# OPENAI_API_KEY = "your_actual_api_key"
openai.api_key = st.secrets["OPENAI_API_KEY"]
# ------------------- TEXT → SPEECH -------------------
st.header("🗣️ Text-to-Speech (TTS)")
text_input = st.text_area("Enter text to convert to speech:")

if st.button("Convert to Speech"):
    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        try:
            tts = gTTS(text_input)
            tts_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(tts_file.name)
            st.audio(tts_file.name, format="audio/mp3")
            tts_file.close()
        except Exception as e:
            st.error(f"Error generating speech: {e}")

# ------------------- SPEECH → TEXT -------------------
st.header("🎧 Speech-to-Text (STT)")
audio_file = st.file_uploader(
    "Upload an audio file (mp3, wav, m4a, ogg)", type=["mp3", "wav", "m4a", "ogg"]
)

MAX_FILE_SIZE_MB = 25

if audio_file is not None:
    size_mb = len(audio_file.getbuffer()) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        st.error(f"File too large! Max size is {MAX_FILE_SIZE_MB} MB.")
    else:
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_audio.write(audio_file.getbuffer())
        temp_audio.close()

        try:
            with open(temp_audio.name, "rb") as f:
                transcript = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=f
                )
            if hasattr(transcript, "text") and transcript.text.strip():
                st.subheader("Transcription Result:")
                st.text(transcript.text)
            else:
                st.warning("Transcription returned empty. Try another audio file.")
        except Exception as e:
            st.error(f"Error transcribing audio: {e}")
        finally:
            os.remove(temp_audio.name)

