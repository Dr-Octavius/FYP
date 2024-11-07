# utils/helper_functions.py

import tempfile
import os
import sounddevice as sd
import wave
import numpy as np

def save_uploaded_file(uploaded_file):
    """Save uploaded file temporarily and return the file path."""
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio.write(uploaded_file.read())
    return temp_audio.name

def record_audio(duration):
    """Record audio from microphone for a specified duration and save to a temporary file."""
    fs = 16000  # Sample rate
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        with wave.open(temp_audio.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # Sample width in bytes for int16
            wf.setframerate(fs)
            wf.writeframes(audio_data.tobytes())
    
    return temp_audio.name
