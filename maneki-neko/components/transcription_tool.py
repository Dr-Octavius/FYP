# components/transcription_tool.py

import os
import streamlit as st
from services.transcription_service import transcribe_audio
from utils.transcription_helper import save_uploaded_file, record_audio

def transcription_tool():
    st.header("Call Transcription")
    
    audio_input_type = st.selectbox("Choose Audio Input", ["Upload a File", "Use Microphone"], key="audio_input_type")

    if audio_input_type == "Upload a File":
        audio_file = st.file_uploader("Upload your audio", type=["wav", "mp3", "m4a"], key="file_uploader")
        
        if st.button("Transcribe Uploaded Audio"):
            if audio_file is not None:
                st.info("Transcribing uploaded audio...")
                audio_file_path = save_uploaded_file(audio_file)
                transcription_text = transcribe_audio(audio_file_path)
                st.success("Transcription complete")
                st.markdown(transcription_text)
                os.remove(audio_file_path)
            else:
                st.error("Please upload an audio file.")

    elif audio_input_type == "Use Microphone":
        duration = st.slider("Recording Duration (seconds)", 1, 60, 5, key="record_duration")
        if st.button("Record and Transcribe Audio"):
            st.info("Recording...")
            audio_file_path = record_audio(duration)
            st.success("Recording complete")
            
            st.info("Transcribing recorded audio...")
            transcription_text = transcribe_audio(audio_file_path)
            st.success("Transcription complete")
            st.markdown(transcription_text)
            
            os.remove(audio_file_path)
