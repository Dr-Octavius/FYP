#!/bin/bash

# Activate your virtual environment if necessary
# source /path/to/your/venv/bin/activate

python3 src/pipeline/train.py
python3 src/pipeline/evaluate.py