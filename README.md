# AI for Sales Pipeline

## Contact Information
- **Full Name**: Loo Wee Sing, Caspian Michael
- **Email**: e0516178@u.nus.edu

## Overview
This repository houses the Artificial Intelligence (AI) for Sales pipeline developed as part of a Final Year Project (FYP). The project aims to enhance the sales efficiency of StaffAny, an HRMS Solutions Company, by automating the sales cycle, from lead generation to deal closing, using AI and Machine Learning (ML).

### Project Structure
```bash
.
├── LICENSE
├── README.md
├── data
│   ├── SA_BE.csv
│   ├── SA_Generic.csv
│   ├── SA_Generic_ContactFilter.csv
│   └── recordings
│       └── recording.mp3
├── eda1.ipynb
├── requirements.txt
├── run.sh
├── saved_models
│   ├── trained_LR_model.pkl
│   ├── trained_RFC_model.pkl
│   └── trained_SVM_model.pkl
└── src
    ├── __init__.py
    ├── config.py
    ├── data_aggregator
    │   ├── getRecording.py
    │   └── transcribeAudio.py
    ├── data_preparation.py
    ├── evaluate.py
    ├── feature_engineering.py
    ├── model.py
    ├── model_preprocessing.py
    └── train.py
```

The `src` directory contains scripts that are part of the ML pipeline:

- `config.py`: Central configuration for the pipeline.
- `data_preparation.py`: Preparing raw data for processing.
- `data_preprocessing.py`: Preprocessing data for ML readiness.
- `feature_engineering.py`: Crafting features based on domain knowledge.
- `model.py`: ML model definitions and utilities.
- `train.py`: Training ML models on processed data.
- `evaluate.py`: Evaluating ML models against test data.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Adjust configurations: Modify `src/config.py` as needed.
3. Train the model: `python src/train.py`
4. Evaluate the model: `python src/evaluate.py`

## Pipeline Overview
1. **Data Ingestion**: Fetch data from various sources.
2. **Data Preparation**: Clean and format raw data.
3. **Data Preprocessing**: Encode, scale, and handle missing values.
4. **Feature Engineering**: Inform feature creation from EDA insights.
5. **Model Training**: Apply algorithms to learn from data.
6. **Model Evaluation**: Assess model performance.

## Key Insights from EDA
The exploratory analysis revealed impactful features and patterns, which were then harnessed in feature engineering to enhance model predictions.

## Categorical Feature Processing
Categorical variables are processed using one-hot encoding to maintain the non-ordinal nature of the data.

## Selected Models
The pipeline includes several ML models known for their performance and interpretability in classification tasks.

## Evaluation Metrics
Model performance is measured using accuracy, precision, recall, and F1 score to balance the trade-offs between false positives and negatives.

## Deployment
Models are intended to be deployed in a cloud environment where they can scale according to the demands of StaffAny's sales data.

## About the FYP
The FYP revolves around the sales cycle of StaffAny, seeking to optimize it with AI/ML interventions. The project leverages data from HubSpot, call recordings, and other sources to build a robust pipeline that forecasts sales outcomes, identifies quality leads, and streamlines the sales process.

For more details on the FYP context and objectives, please refer to the [Project Context](#project-context) section.

## License
This project is open-sourced under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Project Context
[Include detailed project context and abstract here...]

### Problem
[Describe the problem statement here...]

### Scope
[Define the scope here...]

### Objectives
[List the objectives here...]

### Metrics
[Detail the metrics here...]

### Technology Stack
[List and justify the chosen technologies here...]

You should insert the detailed "Project Context," "Problem," "Scope," "Objectives," "Metrics," and "Technology Stack" sections where indicated with placeholders. The context provided will guide the reader through the AI/ML pipeline's purpose, how it integrates with StaffAny's workflow, and the anticipated impact on sales efficiency.