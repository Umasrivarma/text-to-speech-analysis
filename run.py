import streamlit as st
from gtts import gTTS
import tempfile
import os

# Offline Whisper
import whisper

st.set_page_config(page_title="Offline TTS & STT App", layout="centered")
st.title("🎙️ Offline Text-to-Speech & Speech-to-Text App")

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

# ------------------- Speech-to-Text (Offline) -------------------
st.header("🎧 Speech-to-Text (Offline)")
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
            st.info("Transcribing with local Whisper… This may take a while for long audio.")
            model = whisper.load_model("small")  # CPU-friendly model
            result = model.transcribe(temp_audio.name)
            transcript_text = result.get("text", "")
            if transcript_text:
                st.subheader("Transcription Result:")
                st.text(transcript_text)
            else:
                st.warning("Could not transcribe audio.")
        except Exception as e:
            st.error(f"Local Whisper Error: {e}")
        finally:
            os.remove(temp_audio.name)
