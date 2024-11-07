# data_preprocessing.py
import pandas as pd
from config import TARGET_VARIABLE

def preprocess_data(df):
    df_cleaned = df.copy()
    df_cleaned.drop('ID', axis=1, inplace=True)
    df_cleaned = df_cleaned[df_cleaned['Age'] >= 0]
    df_cleaned['Start Smoking'] = pd.to_numeric(df_cleaned['Start Smoking'], errors='coerce')
    df_cleaned['Stop Smoking'] = pd.to_numeric(df_cleaned['Stop Smoking'], errors='coerce')
    
    categorical_columns_with_nan = ['COPD History', 'Air Pollution Exposure', 'Taken Bronchodilators']
    df_cleaned[categorical_columns_with_nan] = df_cleaned[categorical_columns_with_nan].fillna('Unknown')
    
    return df_cleaned
