import streamlit as st
import openai
from gtts import gTTS
import tempfile
import os

# Optional: local Whisper
try:
    import whisper
    local_whisper_available = True
except ImportError:
    local_whisper_available = False

# ------------------- Setup -------------------
st.set_page_config(page_title="TTS & STT App", layout="centered")
st.title("🎙️ Text-to-Speech & Speech-to-Text App")

# 🔐 OpenAI API key from secrets
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
    online_api_available = True
else:
    online_api_available = False

# ------------------- Text-to-Speech -------------------
st.header("🗣️ Text-to-Speech (TTS)")
text_input = st.text_area("Enter text to convert to speech:")
if st.button("Convert to Speech"):
    if text_input.strip():
        try:
            tts = gTTS(text_input)
            tts_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(tts_file.name)
            st.audio(tts_file.name, format="audio/mp3")
            tts_file.close()
        except Exception as e:
            st.error(f"TTS Error: {e}")
    else:
        st.warning("Please enter some text.")

# ------------------- Speech-to-Text -------------------
st.header("🎧 Speech-to-Text (STT)")
audio_file = st.file_uploader("Upload audio (mp3, wav, m4a, ogg)", type=["mp3", "wav", "m4a", "ogg"])

MAX_FILE_SIZE_MB = 25
if audio_file is not None:
    size_mb = len(audio_file.getbuffer()) / (1024*1024)
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
            st.subheader("Transcription Result:")
            st.text(transcript.text)
        except Exception as e:
            st.error(f"Error transcribing audio. Likely cause: quota exceeded or invalid API key.\nDetails: {e}")
        finally:
            os.remove(temp_audio.name)


      


