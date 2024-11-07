from pydub import AudioSegment
import os

# Directory paths
input_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/calls/mp3/batch1'))
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/calls/wav/batch1'))

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def convert_mp3_to_wav(input_path, output_path):
    """Convert a single MP3 file to WAV format."""
    audio = AudioSegment.from_mp3(input_path)
    audio.export(output_path, format="wav")

def batch_convert():
    """Convert all MP3 files in the input directory to WAV format in the output directory."""
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".mp3"):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name.replace(".mp3", ".wav"))
            convert_mp3_to_wav(input_path, output_path)
            print(f"Converted {file_name} to WAV format.")

if __name__ == "__main__":
    batch_convert()
