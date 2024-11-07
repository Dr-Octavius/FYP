# train.py
import pandas as pd
import os
import model_preprocessing as mP
import model as m
import data_preparation as dp
from feature_engineering import add_feature_engineering
from sklearn.model_selection import train_test_split
from src.config import TARGET_VARIABLE,DROP_LIST,MODEL_PATH

def train_model(df, model_save_path, model_type):
    df_staged = mP.encode_categorical_columns(df)
    df_staged = df_staged.drop(columns=DROP_LIST,axis=1)
    X = df_staged.drop(TARGET_VARIABLE, axis=1)
    y = df_staged[TARGET_VARIABLE]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    preprocessor = mP.get_preprocessor(model_type, X_train)
    mP.train_and_save_model(X_train, y_train, model_type, model_save_path, preprocessor)

if __name__ == "__main__":
    # Existing data processing and model training logic here
    df = dp.load_data()
    df_cleaned = dp.clean_data(df)
    df_featured = add_feature_engineering(df_cleaned)
    # Folder where the model will be saved
    model_directory = MODEL_PATH
    
    # Exact location where the model will be saved
    model_save_path = os.path.join(model_directory, "trained_RFC_model.pkl")
    # Ensure the directory exists
    os.makedirs(model_directory, exist_ok=True)
    # Train the model and save it
    train_model(df_featured, model_save_path,m.ModelType.RFC)
    
    # Exact location where the model will be saved
    model_save_path = os.path.join(model_directory, "trained_LR_model.pkl")
    # Ensure the directory exists
    os.makedirs(model_directory, exist_ok=True)
    # Train the model and save it
    train_model(df_featured, model_save_path,m.ModelType.LR)
    
    # Exact location where the model will be saved
    model_save_path = os.path.join(model_directory, "trained_SVM_model.pkl")
    # Ensure the directory exists
    os.makedirs(model_directory, exist_ok=True)
    # Train the model and save it
    train_model(df_featured, model_save_path,m.ModelType.SVM)
