import streamlit as st
from gtts import gTTS
import tempfile
import openai
import os

# ----------------------------
# Streamlit page setup
# ----------------------------
st.set_page_config(page_title="Text ↔ Speech Converter", page_icon="🎙️", layout="centered")
st.title("🎙️ Text ↔ Speech Converter")

# ----------------------------
# OpenAI API Key (required for STT)
# ----------------------------
st.sidebar.header("OpenAI API Key")
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

if not openai_api_key:
    st.warning("⚠️ Enter your OpenAI API key in the sidebar to enable Speech-to-Text")
    st.stop()

openai.api_key = openai_api_key

# ----------------------------
# TEXT TO SPEECH
# ----------------------------
st.header("🗨️ Text → Speech")

text_input = st.text_area("Enter text to convert:", placeholder="Type something...")

if st.button("🔊 Convert to Speech"):
    if text_input.strip():
        tts = gTTS(text_input)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        st.audio(temp_file.name, format="audio/mp3")
        st.success("✅ Speech generated successfully!")
    else:
        st.warning("Please enter some text.")

# ----------------------------
# SPEECH TO TEXT
# ----------------------------
st.header("🎤 Speech → Text")

uploaded_audio = st.file_uploader("Upload an audio file (mp3, wav, m4a):", type=["mp3","wav","m4a"])

if uploaded_audio:
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_audio.write(uploaded_audio.read())
    temp_audio.close()

    st.audio(temp_audio.name, format=f"audio/{uploaded_audio.type.split('/')[-1]}")

    if st.button("📝 Transcribe Audio"):
        with st.spinner("Transcribing audio using OpenAI Whisper API..."):
            try:
                with open(temp_audio.name, "rb") as audio_file:
                    transcript = openai.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                st.success("✅ Transcription complete!")
                st.subheader("🧾 Transcribed Text")
                st.write(transcript.text)
            except Exception as e:
                st.error(f"❌ Error transcribing audio: {e}")

    os.remove(temp_audio.name)

st.markdown("---")
st.markdown("✨ Built with Streamlit, gTTS & OpenAI Whisper API ✨")
