import whisper
import os
import time
import re
from tqdm import tqdm
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, default="tiny", help="Model type for Whisper")
args = parser.parse_args()

temperature=[0.0, 0.2, 0.5]

# Load Whisper model
model = whisper.load_model(args.model)

# Paths
preprocessed_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/calls/cleaned/batch1-chunked'))
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../data/call_transcripts/batch1-chunked/whisper/{args.model}'))
os.makedirs(output_dir, exist_ok=True)

# Function to extract the numeric part of the filename
def get_chunk_number(file_name):
    # Match the last number in the filename before the extension (e.g., "chunk_8.wav" -> 8)
    match = re.search(r'(\d+)(?=\.\w+$)', file_name)
    return int(match.group()) if match else float('inf')

def transcribe_audio(audio_path, language):
    """Transcribe a single audio file in the specified language."""
    task = "translate" if language != "en" else "transcribe"
    result = model.transcribe(audio_path, language=language, temperature=temperature, task=task, fp16=False)
    return result["segments"]

def merge_transcriptions(en_segments, zh_segments):
    combined_transcription = []
    i, j = 0, 0
    while i < len(en_segments) and j < len(zh_segments):
        en_segment = en_segments[i]
        zh_segment = zh_segments[j]
        
        # Check for overlap based on timestamps
        if en_segment["start"] <= zh_segment["end"] and zh_segment["start"] <= en_segment["end"]:
            combined_transcription.append({
                "start": min(en_segment["start"], zh_segment["start"]),
                "end": max(en_segment["end"], zh_segment["end"]),
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
                "english_text": en_segment["text"],
                "mandarin_text": ""
            })
            i += 1
        else:
            # Mandarin segment ends before English segment starts
            combined_transcription.append({
                "start": zh_segment["start"],
                "end": zh_segment["end"],
                "english_text": "",
                "mandarin_text": zh_segment["text"]
            })
            j += 1

    # Append any remaining segments
    while i < len(en_segments):
        en_segment = en_segments[i]
        combined_transcription.append({
            "start": en_segment["start"],
            "end": en_segment["end"],
            "english_text": en_segment["text"],
            "mandarin_text": ""
        })
        i += 1
    while j < len(zh_segments):
        zh_segment = zh_segments[j]
        combined_transcription.append({
            "start": zh_segment["start"],
            "end": zh_segment["end"],
            "english_text": "",
            "mandarin_text": zh_segment["text"]
        })
        j += 1

    return combined_transcription

def format_timestamp(seconds):
    """Convert seconds to a formatted timestamp string."""
    milliseconds = int(seconds * 1000)
    hours = milliseconds // 3_600_000
    milliseconds %= 3_600_000
    minutes = milliseconds // 60_000
    milliseconds %= 60_000
    seconds = milliseconds // 1_000
    milliseconds %= 1_000
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

def transcribe_chunks_sequential(chunks: list, language: str, adjust_timestamps: bool):
    """Transcribe each chunk in sequence for a specific language and combine transcriptions with timestamp adjustment."""
    transcription_segments = []
    cumulative_offset = 0.0
    for i, chunk_path in enumerate(chunks, 1):
        audio = whisper.load_audio(chunk_path)
        chunk_duration = audio.shape[0] / 16000
        try:
            chunk_transcription = transcribe_audio(chunk_path, language)
            for transcript_segment in chunk_transcription:
                if adjust_timestamps:
                    transcript_segment["start"] += cumulative_offset
                    transcript_segment["end"] += cumulative_offset
            cumulative_offset += chunk_duration
            transcription_segments.extend(chunk_transcription)
            print(f"Completed {language} transcription for chunk {i}/{len(chunks)}: {os.path.basename(chunk_path)}")
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

            start_time = time.time()

            # Transcribe in both languages
            print(f"Starting English transcription for {folder_name}...")
            en_transcription = transcribe_chunks_sequential(chunks, language="en",adjust_timestamps=adjust_timestamps)
            print(f"English transcription for {folder_name} complete.")
            print(f"Starting Mandarin transcription for {folder_name}...")
            zh_transcription = transcribe_chunks_sequential(chunks, language="zh",adjust_timestamps=adjust_timestamps)
            print(f"Mandarin transcription for {folder_name} complete.")

            # Merge transcriptions - Uncomment if we go down the Chinese + English Transcription Route
            combined_transcription = merge_transcriptions(en_transcription, zh_transcription)

            # Save combined transcription
            output_path = os.path.join(output_dir, f"{folder_name}.txt")
            with open(output_path, "w") as f:
                # For loop if using English + Translate
                for segment in combined_transcription:
                    start = format_timestamp(segment["start"])
                    end = format_timestamp(segment["end"])
                    en_text = segment["english_text"].strip()
                    zh_text = segment["mandarin_text"].strip()
                    f.write(f"[START:{start}]\t[END:{end}]\t[ENGLISH:{en_text}]\t[MANDARIN:{zh_text}]\n")
            print(f"Transcription for {folder_name} saved.")

            elapsed_time = time.time() - start_time
            print(f"Completed transcription for {folder_name} in {elapsed_time:.2f} seconds.\n")

if __name__ == "__main__":
    batch_transcribe()