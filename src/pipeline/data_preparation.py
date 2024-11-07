import pandas as pd
import numpy as np
from src.config import DATABASE_PATH

def clean_data(df):
    working_df = df.copy()
    
    # Dealing with NaN Values
    for item in working_df.columns:
        if (working_df[item].dtype == 'object'):
            working_df[item] = working_df[item].fillna("unknown")
        elif (working_df[item].dtype == np.float64):
            working_df[item] = working_df[item].fillna(0)
        else:
            continue
    
    # Dealing with float64 Values
    float64_to_int64_columns = [
        'Number of Associated Contacts',
        'Number of times contacted',
    ]

    for item in float64_to_int64_columns:
        working_df[item] = working_df[item].astype(np.int64)
    
    # Converting unknown object types to string
    known_columns = [
        'Record ID',
        'Likelihood to close',
        'Number of Associated Contacts',
        'Number of times contacted',
        'Parent CompanyIDs'
    ]

    for item in working_df.columns:
        if item not in known_columns:
            working_df[item] = working_df[item].astype('string')

    # Converting delimited strings to lists
    semicolon_list_conversion_columns = [
        'Associated Contact',
        'Associated Contact IDs',
        'Deal with Primary Company',
        'Deal with Primary CompanyIDs',
        'Associated Note',
        'Associated Note IDs',
        'Child Company',
        'Child CompanyIDs',
        'Parent Company',
        'Billing Entities',
        'Billing EntitiesIDs',
        'Ideal Customer Profile',
        'Campaign'
    ]

    comma_list_conversion_columns = [
    ]

    for item in semicolon_list_conversion_columns:
        working_df[item] = working_df[item].str.split(';')

    for item in comma_list_conversion_columns:
        working_df[item] = working_df[item].str.split(',')

    # Handling dateTime Columns  
    date_columns_format1 = [
        'Last Activity Date',  
        'First Deal Created Date', 
        'Last Logged Call Date',
        'First Contact Create Date',
        'Create Date'
    ]

    date_columns_format2 = [
        'Churn Date'
    ]

    for col in date_columns_format1:
        working_df[col] = pd.to_datetime(working_df[col], errors='coerce', format='%Y-%m-%d %H:%M')
    for col in date_columns_format2:
        working_df[col] = pd.to_datetime(working_df[col], errors='coerce', format='%Y-%m-%d')
    
    #Remove all the BE Entries
    cleaned_df = working_df[~working_df['Company name'].str.contains('[BE]')].copy()
    
    return cleaned_df

def load_data():
    data_types = {
        'Parent CompanyIDs': 'Int64',  # or use 'float' as needed
    }
    df = pd.read_csv(DATABASE_PATH, dtype=data_types)
    return df