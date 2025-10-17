import streamlit as st
from gtts import gTTS
import os
import io
import tempfile
from pydub import AudioSegment
import speech_recognition as sr


st.set_page_config(page_title="Speech ↔ Text Converter", page_icon="🎙️", layout="centered")
st.title("🎙️ Text ↔ Speech Converter")

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
    # Convert uploaded file to WAV format for recognition
    audio_bytes = uploaded_audio.read()
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)

    st.audio(wav_io, format="audio/wav")

    if st.button("📝 Transcribe Audio"):
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)

        with st.spinner("Transcribing..."):
            try:
                text_output = recognizer.recognize_google(audio_data)
                st.success("✅ Transcription complete!")
                st.subheader("Transcribed Text:")
                st.write(text_output)
            except sr.UnknownValueError:
                st.error("⚠️ Could not understand the speech.")
            except sr.RequestError:
                st.error("⚠️ Network error — please try again later.")

st.markdown("---")
st.markdown("✨ Built with Streamlit, gTTS & SpeechRecognition ✨")

