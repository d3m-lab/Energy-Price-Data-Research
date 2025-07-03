
import os
import pandas as pd
import re

input_folder = "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Raw/Canada/Ontario"
output_folder = "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Processed/Canada/Ontario"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get list of all CSV files in the input folder
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

for filename in csv_files:
    filepath = os.path.join(input_folder, filename)

    # Extract year from the filename
    year_match = re.search(r'_(\d{4})_', filename)
    if year_match:
        year = year_match.group(1)
    else:
        print(f"Year not found in filename: {filename}. Skipping.")
        continue

    try:
        # Read the CSV file
        df = pd.read_csv(filepath, skiprows=3)

        # Ensure required columns exist
        if 'Date' not in df.columns or 'Hour' not in df.columns or 'HOEP' not in df.columns:
            print(f"Required columns ('Date', 'Hour', 'HOEP') not found in {filename}. Skipping.")
            continue

        # Create DateTime column
        # Convert 'Date' to datetime objects
        df['Date'] = pd.to_datetime(df['Date'])
        # Subtract 1 from 'Hour' and convert to integers
        df['Hour'] = df['Hour'].astype(int) - 1
        # Combine 'Date' and 'Hour' to create 'DateTime'
        df['DateTime'] = df.apply(lambda row: row['Date'] + pd.Timedelta(hours=row['Hour']), axis=1)
        # Add 1 day to the 'DateTime' column
        #df['DateTime'] = df['DateTime'] + pd.Timedelta(days=1)


        # Create the new dataframe with required columns
        new_df = pd.DataFrame()
        new_df['DateTime'] = df['DateTime']
        new_df['Price'] = df['HOEP']

        # Define the output filename and path
        output_filename = f"{year}.csv"
        output_filepath = os.path.join(output_folder, output_filename)

        # Save the new dataframe to a CSV file
        new_df.to_csv(output_filepath, index=False)
        print(f"Processed {filename} and saved to {output_filepath}")

    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("Finished processing all CSV files.")
