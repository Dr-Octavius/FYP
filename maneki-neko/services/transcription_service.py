# services/transcription_service.py

import whisper
import streamlit as st

# Load Whisper model
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

def transcribe_audio(audio_path):
    """Transcribe audio file using Whisper model."""
    transcription = model.transcribe(audio_path)
    return transcription["text"]
