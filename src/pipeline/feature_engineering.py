import pandas as pd

# feature_engineering.py
def add_feature_engineering(df):
    df = add_counts(df)
    df = add_BE_logic(df)
    df = add_first_sales_cycle(df)
    df = add_history_delta(df)
    df = add_year_known(df)
    return df

def add_counts(df):
    list_columns = [
        'Campaign',
        'Deal with Primary Company'
    ]
    for col in list_columns:
        df[col + '_count'] = df[col].apply(lambda x: len(x) if isinstance(x, list) and not (len(x) == 1 and x[0] == 'unknown') else 0)
    
    return df

def add_BE_logic(df):
    # Step 1: Create a mask for entries that are [BE] companies
    be_mask = df['Company name'].str.contains('[BE]')

    # Step 2: Filter DataFrame for [BE] companies
    be_companies = df[be_mask]

    # Step 3: Map [BE] companies back to their primary companies
    # Assuming 'Primary CompanyIDs' links back to 'Record ID' of the original company
    be_mapping = be_companies.groupby('Parent CompanyIDs').size()

    # Step 4: Merge this count back to the original DataFrame
    df['BE_count'] = df['Record ID'].map(be_mapping).fillna(0).astype('int64')

    return df

def add_first_sales_cycle(df):
    # Now, subtract the columns to create the new duration column
    df['First_Sales_Cycle_Duration'] = df['First Deal Created Date'] - df['First Contact Create Date']

    # Converting seconds to days
    df['First_Sales_Cycle_Duration'] = df['First_Sales_Cycle_Duration'].dt.total_seconds() / (60*60*24)

    return df

def add_history_delta(df):
    # Now, subtract the columns to create the new duration column
    df['History_delta'] = df['Last Activity Date'] - df['First Contact Create Date']

    # Converting seconds to days
    df['History_delta'] = df['History_delta'].dt.total_seconds() / (60*60*24)
    return df

def add_year_known(df):
    # Step 2: Extract the year from 'Create Date'
    df['Year'] = df['Create Date'].dt.year
    return df