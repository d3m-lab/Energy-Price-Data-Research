

import os
import pandas as pd


base_input_path = "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Raw/Singapore"
base_output_path = "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Processed/Singapore"
# Get a list of all folders in the base input path

folders = [f for f in os.listdir(base_input_path) if os.path.isdir(os.path.join(base_input_path, f))]

for folder in folders:
  # Extract the year from the folder name (last four digits)
  year = folder[-4:]
  print(f"Processing year: {year}")
  # Construct the full path to the current year's folder
  year_folder_path = os.path.join(base_input_path, folder)
  # Get a list of all CSV files in the current year's folder
  csv_files = [f for f in os.listdir(year_folder_path) if f.endswith('.csv')]
  all_year_data = pd.DataFrame()
  for csv_file in csv_files:
    file_path = os.path.join(year_folder_path, csv_file)
    print(f"  Reading file: {csv_file}")
    try:
      df = pd.read_csv(file_path)
      # Rename columns to lowercase for easier access
      df.columns = [col.lower() for col in df.columns]
      # Select and rename relevant columns
      df_processed = df[['date', 'period', 'wep ($/mwh)']].copy()
      df_processed.rename(columns={'wep ($/mwh)': 'Price'}, inplace=True)
      # Convert 'date' to datetime objects
      df_processed['date'] = pd.to_datetime(df_processed['date'])
      #df_processed['date'] = pd.to_datetime(df_processed['date'], format='%d %b %Y')
      # Calculate 'DateTime'
      # Subtract 1 from Period, divide by 2, and take the integer part
      #df_processed['hour'] = ((df_processed['period'] - 1) / 2).astype(int)
      df_processed['period'] = (df_processed['period'] - 1).astype(int)
      # Combine 'date' and 'hour' to create 'DateTime'
      df_processed['DateTime'] = df_processed.apply(lambda row: row['date'] + pd.Timedelta(minutes=30 * row['period']), axis=1)
      # Select only the required columns and reorder them
      df_final = df_processed[['DateTime', 'Price']]
      # Append to the overall dataframe for the year
      all_year_data = pd.concat([all_year_data, df_final], ignore_index=True)
    except Exception as e:
      print(f"    Error processing file {csv_file}: {e}")
  # Sort by DateTime to ensure chronological order
  if not all_year_data.empty:
    all_year_data.sort_values(by='DateTime', inplace=True)
    # Save the merged dataframe to a CSV file
    output_filename = f"{year}.csv"
    output_filepath = os.path.join(base_output_path, output_filename)
    all_year_data.to_csv(output_filepath, index=False)
    print(f"Saved merged data for year {year} to {output_filepath}")
  else:
    print(f"No data processed for year {year}.")