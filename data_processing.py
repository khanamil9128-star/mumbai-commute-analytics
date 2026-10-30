"""
====================================================================
Mumbai Commute Analytics — Step 2: Data Cleaning & Preprocessing
File: data_processing.py
Author: B.Sc Data Science Student Project
====================================================================
Academic Disclaimer:
"This dataset is created/simulated for academic analysis and does not
represent official Mumbai transport statistics."
====================================================================
"""

import os
import pandas as pd
import numpy as np

def clean_commute_data(input_csv="data/commute_data.csv", output_csv="data/commute_data_cleaned.csv"):
    print("=" * 60)
    print("STEP 1: Loading Raw Dataset")
    print("=" * 60)
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"Input file '{input_csv}' not found! Run generate_dataset.py first.")

    df = pd.read_csv(input_csv)
    initial_shape = df.shape
    print(f"Initial Dataset Shape: {initial_shape[0]} rows, {initial_shape[1]} columns\n")

    # 1. Inspect data types and missing values
    print("=" * 60)
    print("STEP 2: Checking Missing Values & Data Types")
    print("=" * 60)
    print(df.isnull().sum())
    print("\nData Types:")
    print(df.dtypes)
    print()

    # 2. Remove Duplicates
    print("=" * 60)
    print("STEP 3: Removing Duplicate Records")
    print("=" * 60)
    dup_count = df.duplicated().sum()
    print(f"Number of duplicate rows found: {dup_count}")
    df = df.drop_duplicates()
    print(f"Shape after removing duplicates: {df.shape}\n")

    # 3. Standardize Transport Mode Strings
    print("=" * 60)
    print("STEP 4: Standardizing Categorical Values (Transport_Mode)")
    print("=" * 60)
    print(f"Unique modes before standardization: {df['Transport_Mode'].unique()}")
    # Capitalize cleanly: 'metro' -> 'Metro', 'LOCAL' -> 'Local', 'auto' -> 'Auto'
    df['Transport_Mode'] = df['Transport_Mode'].astype(str).str.strip().str.capitalize()
    # Handle variations if any
    mode_map = {
        'Metro': 'Metro',
        'Local': 'Local',
        'Auto': 'Auto',
        'Auto rickshaw': 'Auto'
    }
    df['Transport_Mode'] = df['Transport_Mode'].map(mode_map).fillna(df['Transport_Mode'])
    print(f"Unique modes after standardization: {df['Transport_Mode'].unique()}\n")

    # 4. Handle Missing Values
    print("=" * 60)
    print("STEP 5: Handling Missing Values (Imputation)")
    print("=" * 60)
    # Numerical: Waiting_Time_min - Impute using Median (resistant to skew/outliers)
    median_wait = df['Waiting_Time_min'].median()
    df['Waiting_Time_min'] = df['Waiting_Time_min'].fillna(median_wait)
    print(f"Filled missing Waiting_Time_min with median: {median_wait} min")

    # Categorical: Weather - Impute using Mode (most frequent category)
    mode_weather = df['Weather'].mode()[0]
    df['Weather'] = df['Weather'].fillna(mode_weather)
    print(f"Filled missing Weather with mode: '{mode_weather}'\n")

    # 5. Check and Filter Impossible / Negative Values
    print("=" * 60)
    print("STEP 6: Validating Business Rules & Removing Impossible Values")
    print("=" * 60)
    # Travel time must be > 0
    # Cost must be >= 5 (minimum ticket fare)
    # Distance must be > 0.5 km and <= 100 km (within MMR region)
    valid_mask = (
        (df['Cost_INR'] >= 5) &
        (df['Travel_Time_min'] > 0) &
        (df['Distance_km'] > 0.5) &
        (df['Distance_km'] <= 100.0) &
        (df['Waiting_Time_min'] >= 0) &
        (df['Delay_min'] >= 0)
    )
    invalid_count = (~valid_mask).sum()
    print(f"Records violating physical/business rules: {invalid_count}")
    df = df[valid_mask].copy()

    # 6. Detect & Prune Extreme Outliers (Domain-specific for Mumbai Commute)
    print("=" * 60)
    print("STEP 7: Detecting Extreme Outliers")
    print("=" * 60)
    # Auto fares cannot reasonably exceed Rs 1500 for city commutes
    # Local tickets are rarely above Rs 50 for regular single journey
    # Travel time should be realistically < 240 mins (4 hours)
    extreme_cost_mask = (df['Cost_INR'] > 1500)
    extreme_time_mask = (df['Travel_Time_min'] > 240)
    outliers = (extreme_cost_mask | extreme_time_mask).sum()
    print(f"Extreme outliers detected: {outliers}")
    df = df[~(extreme_cost_mask | extreme_time_mask)].copy()

    # 7. Convert Data Types
    print("=" * 60)
    print("STEP 8: Final Data Type Conversion")
    print("=" * 60)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Travel_Time_min'] = df['Travel_Time_min'].astype(int)
    df['Waiting_Time_min'] = df['Waiting_Time_min'].astype(int)
    df['Cost_INR'] = df['Cost_INR'].astype(int)
    df['Delay_min'] = df['Delay_min'].astype(int)
    df['Comfort_Rating'] = df['Comfort_Rating'].astype(int)
    df['Distance_km'] = df['Distance_km'].astype(float)
    df['User_Rating'] = df['User_Rating'].astype(float)

    print("Data types successfully cast to appropriate types.")

    # 8. Save Cleaned Dataset
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print("=" * 60)
    print(f"SUCCESS: Cleaned dataset saved to: {output_csv}")
    print(f"Initial records: {initial_shape[0]} | Final clean records: {len(df)}")
    print(f"Data Cleaning Efficiency: {((initial_shape[0] - len(df)) / initial_shape[0]) * 100:.2f}% noisy rows removed/fixed.")
    print("=" * 60)

    return df

if __name__ == "__main__":
    clean_commute_data()

