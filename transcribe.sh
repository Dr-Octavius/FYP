#!/bin/bash

# Array of model types and corresponding batch sizes and output directories
models=("medium") #"large" "large-v2" "large-v3" "turbo")
batch_sizes=(32) #16 16 16 8)

# Iterate over models, batch sizes, and output directories
for i in ${!models[@]}; do
    model="${models[$i]}"
    batch_size="${batch_sizes[$i]}"

    # Run the Python script with different parameters
    echo "Running transcription with openai-whisper model=$model"
    python3 -m src.call_features.transcribe_whisper \
        --model "$model" 

    Run the Python script with different parameters
    echo "Running transcription with whisperX model=$model, batch_size=$batch_size"
    python3 -m src.call_features.transcribe_whisperX \
        --model "$model"\
        --batch_size "$batch_size" 
done
