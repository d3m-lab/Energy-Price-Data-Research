import os
import pandas as pd
from datetime import datetime
import re
import tqdm
import io

# india data preprocessing

# Specify the directory containing the CSV files
input_directory_india = "D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Raw\India"
output_directory_india = "D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed\India"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory_india):
    os.makedirs(output_directory_india)

all_india_dfs = []

# Iterate through all files in the directory
for filename in os.listdir(input_directory_india):
    if filename.endswith(".csv"):
        filepath = os.path.join(input_directory_india, filename)
        try:
            # Read the CSV file
            df_india = pd.read_csv(filepath)
            #print(df_india)
            print ("Processing: "+ filename)

            # Ensure necessary columns exist
            if 'Delivery Date' not in df_india.columns or 'Time Period' not in df_india.columns or 'Price (Rs./MWh)' not in df_india.columns:
                print(f"Skipping {filename}: Missing required columns.")
                continue

            # Combine "Delivery Date" and first 5 characters of "Time Period" to create "Timestamp" column
            # Need to ensure 'Time Period' is treated as string and 'Delivery Date' as date
            # Assuming 'Time Period' format is something like 'HH:MM - HH:MM'
            # Extracting the first 5 characters usually gives 'HH:MM' of the start time
            df_india['Delivery Date'] = pd.to_datetime(df_india['Delivery Date'],format='%d/%m/%Y', errors='coerce')

            #print(df_india['Delivery Date'].unique())
            #break;
            #exit();
            df_india.dropna(subset=['Delivery Date'], inplace=True) # Drop rows with invalid dates

            df_india['Time Part'] = df_india['Time Period'].astype(str).str[:5]

            # Combine Date and Time part
            df_india['Timestamp_str'] = df_india['Delivery Date'].dt.strftime('%Y-%m-%d') + ' ' + df_india['Time Part']

            # Convert to datetime objects
            df_india['Timestamp'] = pd.to_datetime(df_india['Timestamp_str'], format='%Y-%m-%d %H:%M', errors='coerce')

            # Drop rows where Timestamp could not be created
            df_india.dropna(subset=['Timestamp'], inplace=True)

            # Select and rename columns
            df_india_processed = df_india[['Timestamp', 'Price (Rs./MWh)']].copy()
            df_india_processed = df_india_processed.rename(columns={'Price (Rs./MWh)': 'India'})

            # Append the processed dataframe to the list
            all_india_dfs.append(df_india_processed)

        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Concatenate all dataframes
if all_india_dfs:
    combined_india_df = pd.concat(all_india_dfs).sort_values(by='Timestamp').drop_duplicates(subset='Timestamp').set_index('Timestamp')

    # Extract year from the index (Timestamp)
    combined_india_df['Year'] = combined_india_df.index.year

    # Save the dataframe by year
    for year, df_year in combined_india_df.groupby('Year'):
        # Drop the temporary 'Year' column before saving
        df_to_save = df_year.drop(columns=['Year'])
        output_filename = f"India_IEX_{year}.csv"
        output_filepath = os.path.join(output_directory_india, output_filename)
        df_to_save.to_csv(output_filepath)
        print(f"Saved data for year {year} to {output_filepath}")
else:
    print("No valid CSV files found or processed for India data.")