import pandas as pd
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(raw_data_dir):
    """Loads the E-commerce dataset CSV from the specified directory."""
    logging.info(f"Loading data from {raw_data_dir}...")
    file_path = os.path.join(raw_data_dir, 'Ecommerce_Sales_Data_2024_2025.csv')
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Successfully loaded dataset with shape {df.shape}.")
        return df
    except FileNotFoundError as e:
        logging.error(f"Could not find the dataset at: {file_path}")
        raise

def clean_data(df):
    """Cleans and formats the single dataframe."""
    logging.info("Cleaning data...")
    
    # Clean column names
    df.columns = [col.strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns]
    
    # Expected columns based on peek:
    # order_id, order_date, customer_name, region, city, category, sub_category, 
    # product_name, quantity, unit_price, discount, sales, profit, payment_mode
    
    # Handle missing values
    df.fillna({'category': 'unknown'}, inplace=True)
    
    # Convert dates and extract time features
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        
        logging.info("Extracting time features...")
        df['order_year'] = df['order_date'].dt.year
        df['order_month'] = df['order_date'].dt.month
        df['order_year_month'] = df['order_date'].dt.to_period('M').astype(str)
        df['order_day_of_week'] = df['order_date'].dt.day_name()
    
    # Ensure correct data types for numeric columns
    numeric_cols = ['quantity', 'unit_price', 'discount', 'sales', 'profit']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # For compatibility with subsequent scripts designed for Olist, let's map some names
    # or just use the new ones and we'll update the sql script.
    
    logging.info(f"Cleaned dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")
    return df

def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
    PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
    
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    try:
        raw_df = load_data(RAW_DIR)
        cleaned_df = clean_data(raw_df)
        
        output_path = os.path.join(PROCESSED_DIR, 'ecommerce_cleaned.csv')
        cleaned_df.to_csv(output_path, index=False)
        logging.info(f"Cleaned data saved to {output_path}")
    except Exception as e:
        logging.error(f"Data preparation failed: {e}")

if __name__ == "__main__":
    main()
