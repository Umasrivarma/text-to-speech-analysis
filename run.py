import streamlit as st
import openai
from gtts import gTTS
import os

openai.api_key = "YOUR_KEY"

st.title("Text-to-Speech & Speech-to-Text App")

# ------------------- Text-to-Speech -------------------
st.header("Text-to-Speech")
text_input = st.text_area("Enter text to convert to speech:")
if st.button("Convert to Speech"):
    if text_input:
        tts = gTTS(text_input)
        tts.save("output.mp3")
        st.audio("output.mp3", format="audio/mp3")
    else:
        st.warning("Please enter some text.")

# ------------------- Speech-to-Text -------------------
st.header("Speech-to-Text")
audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])
if audio_file:
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_file.getbuffer())
    try:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=open("temp_audio.wav", "rb")
        )
        st.write("Transcription:")
        st.text(transcript.text)
    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
