import pandas as pd
import re
import os
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset, DataLoader
import torch

# Directory containing folders of transcription .txt files
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/call_transcripts/batch1'))

# Function to load transcriptions from .txt files in the specified folder
def load_transcriptions(data_dir):
    transcriptions = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(data_dir, filename), 'r') as file:
                transcriptions.append(file.read())
    return transcriptions

# Load transcriptions from the directory
transcriptions = load_transcriptions(data_dir)

# Sample class to parse your transcriptions into a structured dataset
class TranscriptionDataset(Dataset):
    def __init__(self, transcriptions, tokenizer, max_length=512):
        self.transcriptions = transcriptions
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.transcriptions)

    def __getitem__(self, idx):
        transcription = self.transcriptions[idx]
        
        # Extract start, end, speaker, English, and Mandarin text fields
        start = re.search(r"\[START:(.*?)\]", transcription).group(1)
        end = re.search(r"\[END:(.*?)\]", transcription).group(1)
        speaker = re.search(r"\[SPEAKER:(.*?)\]", transcription).group(1)
        en_text = re.search(r"\[ENGLISH:(.*?)\]", transcription).group(1)
        zh_text = re.search(r"\[MANDARIN:(.*?)\]", transcription).group(1)
        
        # Prepare inputs (combine English and Mandarin text if applicable)
        input_text = f"{en_text} {zh_text}"
        
        # Tokenize the input
        inputs = self.tokenizer(
            input_text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        # Define labels as needed (e.g., 1 for key feature presence, 0 for absence)
        # Modify label extraction based on specific features you're targeting
        label = 1 if "desired feature" in input_text else 0

        return {
            'input_ids': inputs['input_ids'].squeeze(),
            'attention_mask': inputs['attention_mask'].squeeze(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

# Initialize the tokenizer and model
tokenizer = XLMRobertaTokenizer.from_pretrained("xlm-roberta-base")
model = XLMRobertaForSequenceClassification.from_pretrained("xlm-roberta-base", num_labels=2)

# Prepare the dataset and data loader
dataset = TranscriptionDataset(transcriptions, tokenizer)
train_loader = DataLoader(dataset, batch_size=8, shuffle=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Set up the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models/general_xlm_roberta')))
tokenizer.save_pretrained(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models/general_xlm_roberta')))