<<<<<<< HEAD:src/evaluate.py
=======
import joblib
import pandas as pd
import model_preprocessing as mP
import data_preparation as dp
from src.config import TARGET_VARIABLE,DROP_LIST,MODEL_PATH
from feature_engineering import add_feature_engineering
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
# Assuming you have a module for loading data and/or preprocessing if needed

def load_model(model_path):
    """Load a trained model from the given path."""
    return joblib.load(model_path)

def evaluate_model(X_test, y_test, model):
    """Evaluate the model on the test set and print performance metrics."""
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate and print metrics
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision (Micro): {precision_score(y_test, y_pred, average='micro'):.4f}")
    print(f"Recall (Micro): {recall_score(y_test, y_pred, average='micro'):.4f}")
    print(f"F1 Score (Micro): {f1_score(y_test, y_pred, average='micro'):.4f}")
    print("----------- RESULTS END -----------\n")

def main():
    # Existing data processing and model training logic here
    df = dp.load_data()
    df_cleaned = dp.clean_data(df)
    df_featured = add_feature_engineering(df_cleaned)
    df_staged = mP.encode_categorical_columns(df_featured)
    df_staged = df_staged.drop(columns=DROP_LIST,axis=1)
    
    # use 20% of the data as a training set randomly
    df_test = df_staged.sample(frac=0.2, random_state=42)
    X_test = df_test.drop(TARGET_VARIABLE, axis=1)
    y_test = df_test[TARGET_VARIABLE]
    
    # Load the trained model
    model = load_model(MODEL_PATH+"/trained_RFC_model.pkl")
    
    # Evaluate the model
    print("-------- RFC MODEL RESULTS --------")
    evaluate_model(X_test, y_test, model)
    
    # Load the trained model
    model = load_model(MODEL_PATH+"/trained_LR_model.pkl")
    
    # Evaluate the model
    print("--------  LR MODEL RESULTS --------")
    evaluate_model(X_test, y_test, model)
    
    # Load the trained model
    model = load_model(MODEL_PATH+"/trained_SVM_model.pkl")
    
    # Evaluate the model
    print("-------- SVM MODEL RESULTS --------")
    evaluate_model(X_test, y_test, model)

if __name__ == "__main__":
    main()
>>>>>>> efa0d09 (feat: FYP major commit):src/pipeline/evaluate.py
