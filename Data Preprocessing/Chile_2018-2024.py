
import os
import pandas as pd
from datetime import datetime
import re
import tqdm
import io

# Specify the directory containing the CSV files
input_directory = "D:\OneDrive - The Pennsylvania State University\Research DATA/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Raw/Chile_PreProcessed/Pre_Processed"
output_directory = "D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed\Chile"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

all_dfs = []

# Iterate through all files in the directory
for filename in os.listdir(input_directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(input_directory, filename)
        try:
            # Read the CSV file
            df = pd.read_csv(filepath)

            # Ensure necessary columns exist
            if 'YearMonth' not in df.columns or 'Day' not in df.columns or 'Hour' not in df.columns or 'Zone' not in df.columns or 'CMg[$/KWh]' not in df.columns:
                print(f"Skipping {filename}: Missing required columns.")
                continue

            # Combine YearMonth, Day, and Hour to create Timestamp
            # Handle YearMonth format YYYYMM
            df['Year'] = df['YearMonth'].astype(str).str[:4]
            df['Month'] = df['YearMonth'].astype(str).str[4:]

            # Adjust Hour column (subtract 1)
            df['AdjustedHour'] = df['Hour'] - 1

            # Create a temporary datetime string
            df['DateTime_Str'] = df['Year'] + '-' + df['Month'] + '-' + df['Day'].astype(str) + ' ' + df['AdjustedHour'].astype(str) + ':00:00'

            # Convert to datetime objects, handling potential errors
            df['Timestamp'] = pd.to_datetime(df['DateTime_Str'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

            # Drop rows where Timestamp could not be created
            df.dropna(subset=['Timestamp'], inplace=True)

            # Pivot the table
            df_pivot = df.pivot_table(index='Timestamp', columns='Zone', values='CMg[$/KWh]', aggfunc='first')

            # Append the pivoted dataframe to the list
            all_dfs.append(df_pivot)

        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Concatenate all dataframes
if all_dfs:
    combined_df = pd.concat(all_dfs).sort_index()

    # Extract year from the index (Timestamp)
    combined_df['Year'] = combined_df.index.year

    # Save the dataframe by year
    for year, df_year in combined_df.groupby('Year'):
        # Drop the temporary 'Year' column before saving
        df_to_save = df_year.drop(columns=['Year'])
        output_filename = f"Chile_CEN_{year}.csv"
        output_filepath = os.path.join(output_directory, output_filename)
        df_to_save.to_csv(output_filepath)
        print(f"Saved data for year {year} to {output_filepath}")
else:
    print("No valid CSV files found or processed.")
