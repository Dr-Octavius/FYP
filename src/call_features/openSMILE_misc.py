import os
import opensmile
import pandas as pd

# Load OpenSMILE model
model = opensmile.Smile(
    feature_set=opensmile.FeatureSet.ComParE_2016,
    feature_level=opensmile.FeatureLevel.Functionals
)

# Paths
audio_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/calls/cleaned/batch1'))
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/audio_features/batch1'))
os.makedirs(output_dir, exist_ok=True)

def get_audio_chunks(audio_folder):
    """
    Collect all .wav files in each subdirectory (representing audio chunks).

    Args:
        audio_folder (str): Path to the directory containing folders of audio chunks.

    Returns:
        dict: A dictionary with folder names as keys and lists of .wav file paths as values.
    """
    audio_chunks = {}
    for folder_name in os.listdir(audio_folder):
        folder_path = os.path.join(audio_folder, folder_name)
        if os.path.isdir(folder_path):
            chunks = sorted([
                os.path.join(folder_path, file_name)
                for file_name in os.listdir(folder_path)
                if file_name.endswith(".wav")
            ])
            audio_chunks[folder_name] = chunks
    return audio_chunks

def extract_features(audio_chunks):
    """
    Extract audio features from a dictionary of audio chunks.

    Args:
        audio_chunks (dict): Dictionary with folder names as keys and lists of chunk paths as values.

    Returns:
        pd.DataFrame: DataFrame containing extracted features for each audio chunk.
    """
    all_features = []
    for folder_name, chunks in audio_chunks.items():
        print(f"Extracting features for {folder_name}...")
        for chunk_path in chunks:
            features = model.process_file(chunk_path)
            features['filename'] = folder_name
            all_features.append(features)
    return pd.concat(all_features, ignore_index=True)

def batch_extract():
    # Get audio chunks from folders
    audio_chunks = get_audio_chunks(audio_folder)

    # Extract features
    features_df = extract_features(audio_chunks)

    # Save to CSV
    """Save extracted features DataFrame to a CSV file."""
    output_file = os.path.join(output_dir, 'audio_features.csv')
    features_df.to_csv(output_file, index=False)
    print(f"Features saved to {output_file}")

if __name__ == "__main__":
    batch_extract()