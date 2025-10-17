import streamlit as st
from gtts import gTTS
import os
import whisper

st.title("🧠 Unstructured Data Analysis")

tab1, tab2, tab3 = st.tabs(["🖼️ Image Analysis", "🎧 Audio Analysis", "📝 Text Analysis"])

with tab2:

    # ------------------ TEXT TO SPEECH ------------------
    st.header("🗣️ Text to Speech")
    text = st.text_area("Enter text to convert to speech:")

    if st.button("Convert to Audio"):
        if text.strip():
            tts = gTTS(text, lang='en')
            tts.save("output.mp3")
            audio_file = open("output.mp3", "rb")
            st.audio(audio_file.read(), format='audio/mp3')
            st.success("✅ Conversion complete!")
        else:
            st.warning("Please enter some text.")

    
    # ------------------ SPEECH TO TEXT ------------------
    st.header("🗣️ Speech to Text")

    @st.cache_resource(show_spinner=False)
    def load_whisper_model(model_name="base"):
        return whisper.load_model(model_name)

    model = load_whisper_model("base")
    st.success("✅ Whisper model loaded")


    uploaded_audio = st.file_uploader("Upload an audio file (wav/mp3/m4a)", type=["wav", "mp3", "m4a"])

    if uploaded_audio:
        # Save uploaded audio temporarily
        temp_file_path = "temp_audio." + uploaded_audio.name.split(".")[-1]
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_audio.read())

        st.audio(temp_file_path)


        if st.button("Transcribe Audio"):
            with st.spinner("Transcribing with Whisper..."):
                result = model.transcribe(temp_file_path)

            st.success("✅ Transcription complete!")
            st.subheader("Transcribed Text")
            st.write(result["text"])
