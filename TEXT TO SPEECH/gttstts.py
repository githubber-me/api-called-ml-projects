import streamlit as st
from gtts import gTTS
import os

# Streamlit UI
st.title("Text-to-Speech with gTTS")

# Text input field
text_input = st.text_area("Enter text to convert to speech:")

# Button to generate speech
if st.button("Generate Speech"):

    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        # Language setting (English)
        language = 'en'

        # Generate speech
        tts = gTTS(text=text_input, lang=language, slow=False)

        # Save the speech to a file
        tts.save("output.mp3")

        # Play the audio
        st.audio("output.mp3", format='audio/mp3')
        st.success("Speech generated successfully!")
