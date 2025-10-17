import streamlit as st
from gtts import gTTS
import tempfile
import os
import whisper

st.set_page_config(page_title="Speech ↔ Text Converter", page_icon="🗣️", layout="centered")

st.title("🗣️ Text ↔ Speech Converter")

# =====================
# TEXT TO SPEECH SECTION
# =====================
st.header("🗨️ Text to Speech")

text_input = st.text_area("Enter text you want to convert to speech:", placeholder="Type something...")

if st.button("🎧 Convert to Speech"):
    if text_input.strip():
        with st.spinner("Converting text to speech..."):
            tts = gTTS(text_input)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_file.name)
            st.audio(temp_file.name, format="audio/mp3")
            st.success("✅ Conversion complete!")
    else:
        st.warning("Please enter some text first.")


# =====================
# SPEECH TO TEXT SECTION
# =====================
st.header("🎤 Speech to Text")

audio_file = st.file_uploader("Upload an audio file (MP3, WAV, M4A):", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    with st.spinner("Transcribing speech..."):
        # Save uploaded audio temporarily
        temp_audio = tempfile.NamedTemporaryFile(delete=False)
        temp_audio.write(audio_file.read())
        temp_audio_path = temp_audio.name

        # Load Whisper model
        model = whisper.load_model("base")

        # Transcribe
        result = model.transcribe(temp_audio_path)
        transcription = result["text"]

        st.subheader("🧾 Transcription Result:")
        st.write(transcription)

        os.remove(temp_audio_path)

st.markdown("---")
st.markdown("🔹 Developed with ❤️ using Streamlit, gTTS, and Whisper")
