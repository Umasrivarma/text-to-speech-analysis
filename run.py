import streamlit as st
from gtts import gTTS
import os
import io
import tempfile
import speech_recognition as sr

st.set_page_config(page_title="Speech ↔ Text Converter", page_icon="🎙️", layout="centered")
st.title("🎙️ Text ↔ Speech Converter")


text = st.text_area("Enter text to convert to speech:")

if st.button("Convert to Audio"):
    if text.strip():
        tts = gTTS(text)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        st.audio(temp_file.name, format="audio/mp3")
        st.success("✅ Conversion complete!")
    else:
        st.warning("Please enter some text.")

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
        st.warning("Please enter text first.")

# ----------------------------
# SPEECH TO TEXT
# ----------------------------
st.header("🎤 Speech → Text")

uploaded_audio = st.file_uploader("Upload an audio file (wav, mp3, m4a):", type=["wav", "mp3", "m4a"])

if uploaded_audio is not None:
    # Save uploaded file temporarily
    temp_audio = tempfile.NamedTemporaryFile(delete=False)
    temp_audio.write(uploaded_audio.read())
    temp_audio_path = temp_audio.name

    st.audio(temp_audio_path, format=f"audio/{uploaded_audio.type.split('/')[-1]}")

    if st.button("📝 Transcribe Audio"):
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = recognizer.record(source)

        with st.spinner("Transcribing..."):
            try:
                text_output = recognizer.recognize_google(audio_data)
                st.success("✅ Transcription complete!")
                st.subheader("🧾 Transcribed Text:")
                st.write(text_output)
            except sr.UnknownValueError:
                st.error("⚠️ Could not understand the speech.")
            except sr.RequestError:
                st.error("⚠️ Network error — please try again later.")

    os.remove(temp_audio_path)

st.markdown("---")
st.markdown("✨ Built with Streamlit, gTTS & SpeechRecognition ✨")

