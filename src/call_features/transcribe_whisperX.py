import whisperx
import time
import gc
import os
import re
from tqdm import tqdm
from src.config import HUGGINGFACE_TOKEN
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, default="tiny", help="Model type for WhisperX")
parser.add_argument("--batch_size", type=int, default=16, help="Batch size for WhisperX")
args = parser.parse_args()

device = "cpu" 
batch_size = args.batch_size # reduce if low on GPU mem
compute_type = "float32" # change to "int8" if low on GPU mem (may reduce accuracy)

# Load Whisper model (consider using a smaller model for speed, e.g., "medium")
model = whisperx.load_model(args.model, device=device, compute_type=compute_type) 

# Paths
preprocessed_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/calls/cleaned/batch1-chunked'))
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../data/call_transcripts/batch1-chunked/whisperX/{args.model}'))
os.makedirs(output_dir, exist_ok=True)

# Function to extract the numeric part of the filename
def get_chunk_number(file_name):
    # Match the last number in the filename before the extension (e.g., "chunk_8.wav" -> 8)
    match = re.search(r'(\d+)(?=\.\w+$)', file_name)
    return int(match.group()) if match else float('inf')

def merge_transcription(english_segments, mandarin_segments):
    combined_transcription = []
    i, j = 0, 0
    while i < len(english_segments) and j < len(mandarin_segments):
        en_segment = english_segments[i]
        zh_segment = mandarin_segments[j]
        
        # Check for overlap based on timestamps
        if en_segment["start"] <= zh_segment["end"] and zh_segment["start"] <= en_segment["end"]:
            combined_transcription.append({
                "start": min(en_segment["start"], zh_segment["start"]),
                "end": max(en_segment["end"], zh_segment["end"]),
                "speaker": en_segment.get("speaker", "Unknown"),
                "english_text": en_segment["text"],
                "mandarin_text": zh_segment["text"]
            })
            i += 1
            j += 1
        elif en_segment["end"] < zh_segment["start"]:
            # English segment ends before Mandarin segment starts
            combined_transcription.append({
                "start": en_segment["start"],
                "end": en_segment["end"],
                "speaker": en_segment.get("speaker", "Unknown"),
                "english_text": en_segment["text"],
                "mandarin_text": ""
            })
            i += 1
        else:
            # Mandarin segment ends before English segment starts
            combined_transcription.append({
                "start": zh_segment["start"],
                "end": zh_segment["end"],
                "speaker": zh_segment.get("speaker", "Unknown"),
                "english_text": "",
                "mandarin_text": zh_segment["text"]
            })
            j += 1

    # Append any remaining segments
    while i < len(english_segments):
        en_segment = english_segments[i]
        combined_transcription.append({
            "start": en_segment["start"],
            "end": en_segment["end"],
            "speaker": en_segment.get("speaker", "Unknown"),
            "english_text": en_segment["text"],
            "mandarin_text": ""
        })
        i += 1
    while j < len(mandarin_segments):
        zh_segment = mandarin_segments[j]
        combined_transcription.append({
            "start": zh_segment["start"],
            "end": zh_segment["end"],
            "speaker": zh_segment.get("speaker", "Unknown"),
            "english_text": "",
            "mandarin_text": zh_segment["text"]
        })
        j += 1

    return combined_transcription

def format_timestamp(
    seconds: float, always_include_hours: bool = False, decimal_marker: str = "."
):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return (
        f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
    )

def transcribe_audio(audio_path: str, language: str):
    audio = whisperx.load_audio(audio_path)
    # switch to just using english to test accuracy
    task = "translate" if language != "en" else "transcribe"
    result = model.transcribe(audio_path, language=language, batch_size=batch_size, task=task)
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    aligned_result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=HUGGINGFACE_TOKEN, device=device)
    diarize_segments = diarize_model(audio,max_speakers=2,min_speakers=1)
    diarize_result = whisperx.assign_word_speakers(diarize_segments, aligned_result)
    return diarize_result["segments"]

def transcribe_chunks_sequential(chunks: list, language: str, adjust_timestamps: bool):
    """Transcribe each chunk in sequence for a specific language and combine transcriptions with timestamp adjustment."""
    transcription_segments = []
    cumulative_offset = 0.0
    for i, chunk_path in enumerate(chunks, 1):
        audio = whisperx.load_audio(chunk_path)
        chunk_duration = audio.shape[0] / 16000
        try:
            chunk_segments = transcribe_audio(chunk_path, language)
            for transcript_segment in chunk_segments:
                if adjust_timestamps:
                    transcript_segment["start"] += cumulative_offset
                    transcript_segment["end"] += cumulative_offset
            cumulative_offset += chunk_duration
            transcription_segments.extend(chunk_segments)
            print(f"Completed chunk {i}/{len(chunks)}: {os.path.basename(chunk_path)}")
            # Clear memory to avoid CPU overload
            gc.collect()
        except Exception as e:
            print(f"Error processing chunk {os.path.basename(chunk_path)}: {e}")
    return transcription_segments

def batch_transcribe():
    for folder_name in tqdm(os.listdir(preprocessed_dir)):
        folder_path = os.path.join(preprocessed_dir, folder_name)
        
        # Check if folder_path is a directory (where chunks are stored)
        if os.path.isdir(folder_path):
            print(f"Transcribing {folder_name}...")
            # Gather all chunk files in order
            chunks = sorted(
                [os.path.join(folder_path, file_name) 
                for file_name in os.listdir(folder_path) if file_name.endswith(".wav")],
                key=lambda x: get_chunk_number(os.path.basename(x))
            )
            if len(chunks) == 1:
                adjust_timestamps = False
            else:
                adjust_timestamps = True

            # Estimate start time for progress tracking
            start_time = time.time()

            # Transcribe
            print(f"Starting English transcription for {folder_name}...")
            en_transcription = transcribe_chunks_sequential(chunks,"en",adjust_timestamps)
            print(f"English Transcription for {folder_name} complete.")
            print(f"Starting Mandarin transcription for {folder_name}...")
            zh_transcription = transcribe_chunks_sequential(chunks,"zh",adjust_timestamps)
            print(f"Mandarin Transcription for {folder_name} complete.")

            # Merge transcriptions - Uncomment if we go down the Chinese + English Transcription Route
            combined_transcription = merge_transcription(en_transcription, zh_transcription)

            # Save combined transcription
            output_path = os.path.join(output_dir, f"{folder_name}.txt")
            with open(output_path, "w") as f:
                # For loop if using English + Translate
                for segment in combined_transcription:
                    start = format_timestamp(segment["start"])
                    end = format_timestamp(segment["end"])
                    speaker = segment.get("speaker", "Unknown")
                    en_text = segment["english_text"].strip()
                    zh_text = segment["mandarin_text"].strip()
                    f.write(f"[START:{start}]\t[END:{end}]\t[SPEAKER:{speaker}]\t[ENGLISH:{en_text}]\t[MANDARIN:{zh_text}]\n")
            print(f"Transcription for {folder_name} saved.")

            # Progress tracking
            elapsed_time = time.time() - start_time
            print(f"Completed transcription for {folder_name} in {elapsed_time:.2f} seconds.\n")

if __name__ == "__main__":
    batch_transcribe()