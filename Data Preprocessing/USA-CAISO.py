

import os
import pandas as pd

input_folder = "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Raw/USA/CAISO"
output_folder = "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Processed/USA/CAISO"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# List all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder, filename)

        # Extract the year from the filename (first 4 characters)
        year = filename[:4]

        # Read the CSV file into a DataFrame
        try:
            df = pd.read_csv(file_path,parse_dates=['Date'])
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue

        # Check if necessary columns exist
        if 'Date' not in df.columns or 'zone' not in df.columns or 'price' not in df.columns:
            print(f"Skipping {filename}: Missing required columns (Date, zone, or price).")
            continue

        # Apply pivot table
        try:
            pivot_df = df.pivot_table(index='Date', columns='zone', values='price', aggfunc='first')
        except Exception as e:
            print(f"Error creating pivot table for {filename}: {e}")
            continue

        # Define the output path for the processed CSV
        output_filename = f"{year}.csv"
        output_path = os.path.join(output_folder, output_filename)

        # Save the pivot table to a CSV file
        try:
            pivot_df.to_csv(output_path)
            print(f"Processed and saved {filename} to {output_path}")
        except Exception as e:
            print(f"Error saving processed data for {filename} to {output_path}: {e}")

print("Processing complete.")
