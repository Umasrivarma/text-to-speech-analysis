import streamlit as st
import openai
from gtts import gTTS
import tempfile
import os

# ------------------- OpenAI API Key -------------------
openai.api_key = "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"  # Replace YOUR_KEY with your OpenAI API key

st.title("Text-to-Speech & Speech-to-Text App")

# ------------------- Text-to-Speech -------------------
st.header("Text-to-Speech (TTS)")

text_input = st.text_area("Enter text to convert to speech:")
if st.button("Convert to Speech"):
    if text_input.strip() != "":
        tts = gTTS(text_input)
        tts_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tts_file.name)
        st.audio(tts_file.name, format="audio/mp3")
        tts_file.close()
    else:
        st.warning("Please enter some text to convert.")

# ------------------- Speech-to-Text -------------------
st.header("Speech-to-Text (STT)")

audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a", "ogg"])
if audio_file is not None:
    # Save the uploaded file temporarily
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_audio.write(audio_file.getbuffer())
    temp_audio.close()

    try:
        # Transcribe using OpenAI Whisper
        with open(temp_audio.name, "rb") as f:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        st.subheader("Transcription:")
        st.text(transcript.text)
    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
    finally:
        os.remove(temp_audio.name)  # Clean up temp file
