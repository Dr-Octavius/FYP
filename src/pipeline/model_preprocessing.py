# df_preprocessing.py
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV
import joblib
import model as m

def encode_categorical_columns(df):
    df = encode_ICP(df)
    df = encode_BE(df)
    df = encode_year(df)
    df = encode_industry(df)
    return df

def encode_ICP(df):
    """
    Encodes categorical columns in the DataFrame.
    
    Parameters:
    - df: A pandas DataFrame.
    - columns_to_encode: A list of column names to encode.
    
    Returns:
    - df_encoded: A DataFrame with encoded columns.
    """
    # List of categories based on your images
    all_categories = [
        'ICP1 (Owner with 1 outlet)',
        'ICP2 (Owner with >1 outlets)',
        'ICP3 (Owner with outlet managers)',
        'ICP4 (Owner with HR Executive)',
        'ICP5 (Owner with HR Executive and Ops Manager)',
        'ICP6 (Owner with HR Team and Area Manager)',
        'ICP7 (CEO with Ops and HR Director)',
        'Partner (Integrator)',
        'Partner (Others)',
        'Partner (Reseller)'
    ]

    # One-hot encoding
    for category in all_categories:
        # Sanitize the category to create a valid column name
        column_name = category.replace(' ', '_').replace('>', 'gt').replace('(', '').replace(')', '')
        df[column_name] = df['Ideal Customer Profile'].apply(lambda x: int(category in x) if isinstance(x, list) else 0)
    
    return df

def encode_BE(df):
    df['BE_Indicator'] = df['BE_count'].apply(lambda x: 1 if x else 0)
    return df

def encode_year(df):
    # Step 3: One-hot encode the year
    year_dummies = pd.get_dummies(df['Year'], prefix='Year')

    # Step 4: Concatenate the original DataFrame with the new one-hot encoded columns
    df = pd.concat([df, year_dummies], axis=1)
    return df

def encode_industry(df):
    # Step 3: One-hot encode the year
    industry_dummies = pd.get_dummies(df['Industry (StaffAny Official)'], prefix='Industry')

    # Step 4: Concatenate the original DataFrame with the new one-hot encoded columns
    df = pd.concat([df, industry_dummies], axis=1)
    return df

def get_preprocessor(model_type, X_train):
    """Return the appropriate preprocessor based on the model type."""
    if model_type in [m.ModelType.LR, m.ModelType.SVM]:
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])
        numerical_columns = X_train.select_dtypes(include=['int64', 'float64']).columns
        preprocessor = ColumnTransformer(
            transformers=[('num', numeric_transformer, numerical_columns)],
            remainder='passthrough'
        )
    else:
        preprocessor = None  # No preprocessing or define default
    return preprocessor

def train_and_save_model(X_train, y_train, model_type, model_save_path, preprocessor=None):
    """Train the model and save it to the specified path."""
    if preprocessor:
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', m.get_model_by_type(model_type))
        ])
    else:
        pipeline = m.get_model_by_type(model_type)  # Directly use model if no preprocessor
    
    pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, model_save_path)
    print(f"Model trained and saved successfully to {model_save_path}.")