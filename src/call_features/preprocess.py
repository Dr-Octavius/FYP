import os
import soundfile as sf
import librosa
from pydub import AudioSegment

# Paths
input_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/calls/wav/batch1'))
preprocessed_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/calls/cleaned/batch1-chunked'))
os.makedirs(preprocessed_dir, exist_ok=True)

# Constants
MIN_DURATION_MS = 1000  # Minimum duration in milliseconds
TARGET_SAMPLE_RATE = 16000  # Whisper's preferred sample rate
MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024 # File size limit in bytes (25 MB)
CHUNK_DURATION_MS = 30 * 1000 # 30 seconds in milliseconds
SPLIT_ON_SIZE = False
SPLIT_ON_DURATION = True

def reduce_noise(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    y_reduced = librosa.effects.preemphasis(y)
    temp_path = audio_path.replace(".wav", "_cleaned.wav")
    sf.write(temp_path, y_reduced, sr)
    return temp_path

def normalize_volume(audio_path, target_dBFS=-20.0):
    audio = AudioSegment.from_file(audio_path)
    change_in_dBFS = target_dBFS - audio.dBFS
    normalized_audio = audio.apply_gain(change_in_dBFS)

    # Save normalized audio
    temp_path = audio_path.replace(".wav", "_normalized.wav")
    normalized_audio.export(temp_path, format="wav")
    return temp_path

def prepare_chunk(audio_path):
    """Ensure chunk is mono, 16 kHz, and has minimum duration."""
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_frame_rate(TARGET_SAMPLE_RATE).set_channels(1)
    
    if len(audio) < MIN_DURATION_MS:
        padding = AudioSegment.silent(duration=(MIN_DURATION_MS - len(audio)))
        audio = audio + padding

    # Save prepared chunk
    prepared_path = audio_path.replace(".wav", "_prepared.wav")
    audio.export(prepared_path, format="wav")
    return prepared_path

def split_audio(audio_path, output_folder, max_file_size=MAX_FILE_SIZE_BYTES, chunk_duration_ms=CHUNK_DURATION_MS):
    audio = AudioSegment.from_file(audio_path)
    if SPLIT_ON_SIZE:
        original_size = os.path.getsize(audio_path)
        
        if original_size > max_file_size:
            chunks = []
            approx_chunk_duration = int(len(audio) * (max_file_size / original_size))
            
            for i in range(0, len(audio), approx_chunk_duration):
                chunk = audio[i:i + approx_chunk_duration]
                chunk_path = os.path.join(output_folder, f"chunk_{i // 1000}.wav")
                chunk.export(chunk_path, format="wav")

                # Prepare each chunk to ensure consistency
                prepared_chunk_path = prepare_chunk(chunk_path)
                chunks.append(prepared_chunk_path)
                
                os.remove(chunk_path)
            return chunks
    elif SPLIT_ON_DURATION:
        # Calculate the number of chunks based on the chunk duration
        chunks = []
        for i in range(0, len(audio), chunk_duration_ms):
            chunk = audio[i:i + chunk_duration_ms]
            chunk_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(audio_path))[0]}_chunk_{i // chunk_duration_ms}.wav")
            
            # Export chunk
            chunk.export(chunk_path, format="wav")
            chunks.append(chunk_path)

        return chunks
    else:
        # If no chunking is needed, prepare the whole file as one
        single_chunk_path = os.path.join(output_folder, os.path.basename(audio_path))
        audio = AudioSegment.from_file(audio_path)
        audio.export(single_chunk_path, format="wav")
        prepared_chunk_path = prepare_chunk(single_chunk_path)
        os.remove(single_chunk_path)
        return [prepared_chunk_path]

def preprocess_audio(audio_path):
    file_name = os.path.splitext(os.path.basename(audio_path))[0]
    output_folder = os.path.join(preprocessed_dir, file_name)
    os.makedirs(output_folder, exist_ok=True)

    # Process audio: noise reduction and volume normalization
    cleaned_path = reduce_noise(audio_path)
    normalized_path = normalize_volume(cleaned_path)
    chunks = split_audio(normalized_path, output_folder)
    
    # Cleanup intermediate files
    os.remove(cleaned_path)
    os.remove(normalized_path)
    return chunks

def batch_preprocess():
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".wav"):
            audio_path = os.path.join(input_dir, file_name)
            print(f"Preprocessing {file_name}...")
            preprocess_audio(audio_path)

if __name__ == "__main__":
    batch_preprocess()