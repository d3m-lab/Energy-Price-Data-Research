# prompt: read "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Raw/Europe_New" the folder as input_dir and then read all the folders as country name. then read those country  folder if you find csv files  then combine all the csv files where 1st column will Timestapmp column. however first column has a date string and take the datetime before hypen "-" and format is "%m.%d.%Y %H:%M" but convert to datetime. Second column will be second column .
# if after reading the country folder, if you find out there is more folder then those folder names are zone. merge all the csv files and add a column zone. then first column timestamp will be taken from the first column seperated by hyphen  and take the previous part of it. remmeber date formate is "%m.%d.%Y %H:%M" and need to convert it to datetime. second column will be price from the second column. and zone column will be another. at the end convert zone to column and price will be values.
# then all the out put will be saved to "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Processed/Europe_New" with the country folder then year.csv
import os
import pandas as pd
from datetime import datetime
import re
input_dir = "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Raw/Europe_New"
output_dir = "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Processed/Europe_New"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# List all items in the input directory
country_folders = [item for item in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, item))]

for country_folder in country_folders:
  country_path = os.path.join(input_dir, country_folder)
  print(f"Processing country: {country_folder}")

  # Check for subfolders (zones)
  zone_folders = [item for item in os.listdir(country_path) if os.path.isdir(os.path.join(country_path, item))]

  if zone_folders:
    # Process with zones
    print(f"  Found zones in {country_folder}: {zone_folders}")
    country_data = {} # Dictionary to hold DataFrames for each year, keyed by year

    for zone_folder in zone_folders:
      zone_path = os.path.join(country_path, zone_folder)
      print(f"    Processing zone: {zone_folder}")

      # List all files in the zone folder
      files_in_zone = [f for f in os.listdir(zone_path) if f.endswith('.csv')]

      for file_name in files_in_zone:
        file_path = os.path.join(zone_path, file_name)
        # Assuming filename contains year, e.g., "data_2020.csv" or "zone_data_2021_something.csv"
        # Trying to extract year from filename, adjust pattern as needed
        year_match = re.search(r'(\d{4})', file_name)
        if year_match:
          year = year_match.group(1)
          print(f"      Processing file: {file_name} for year {year}")

          try:
            # Read the CSV file
            df = pd.read_csv(file_path)

            # Ensure the DataFrame has at least 2 columns
            if df.shape[1] < 2:
                print(f"        Skipping file {file_name}: Does not have enough columns.")
                continue

            # Rename the first two columns for clarity
            df.rename(columns={df.columns[0]: 'Timestamp_Str', df.columns[1]: 'Price'}, inplace=True)

            # Extract date and time part before the hyphen and convert to datetime
            df['DateTime'] = df['Timestamp_Str'].apply(
                lambda x: datetime.strptime(x.split('-')[0].strip(), "%d.%m.%Y %H:%M") if '-' in x else None
            )

            # Add Zone column
            df['Zone'] = zone_folder

            # Select only necessary columns
            df_processed = df[['DateTime', 'Price', 'Zone']].copy()

            # Drop rows with NaT in DateTime (if date parsing failed)
            df_processed.dropna(subset=['DateTime'], inplace=True)

            # Group data by year
            if year not in country_data:
              country_data[year] = pd.DataFrame()

            country_data[year] = pd.concat([country_data[year], df_processed], ignore_index=True)

          except Exception as e:
            print(f"        Error processing file {file_name}: {e}")

    # Consolidate and save data for each year for this country with zones
    for year, year_df in country_data.items():
      if not year_df.empty:
        # Pivot the DataFrame to have DateTime as index, Zones as columns, and Price as values
        # Handle potential duplicates or different prices for the same timestamp and zone by taking the mean
        pivot_df = year_df.pivot_table(index='DateTime', columns='Zone', values='Price', aggfunc='first')

        # Sort by DateTime
        pivot_df.sort_index(inplace=True)

        # Define the output file path for this country and year
        country_output_path = os.path.join(output_dir, country_folder)
        os.makedirs(country_output_path, exist_ok=True) # Ensure country output directory exists
        output_filepath = os.path.join(country_output_path, f"{year}.csv")

        # Save the resulting DataFrame to a CSV file
        pivot_df.to_csv(output_filepath)
        print(f"  Saved processed data for {country_folder} - {year} to {output_filepath}")
      else:
        print(f"  No data processed for {country_folder} - {year}")


  else:
    # Process without zones (direct CSV files in country folder)
    print(f"  No zones found in {country_folder}. Processing CSVs directly.")
    country_data = {} # Dictionary to hold DataFrames for each year, keyed by year

    # List all CSV files in the country folder
    files_in_country = [f for f in os.listdir(country_path) if f.endswith('.csv')]

    for file_name in files_in_country:
      file_path = os.path.join(country_path, file_name)
      # Assuming filename contains year
      year_match = re.search(r'(\d{4})', file_name)
      if year_match:
        year = year_match.group(1)
        print(f"    Processing file: {file_name} for year {year}")

        try:
          # Read the CSV file
          df = pd.read_csv(file_path)

          # Ensure the DataFrame has at least 2 columns
          if df.shape[1] < 2:
              print(f"      Skipping file {file_name}: Does not have enough columns.")
              continue

          # Rename the first two columns for clarity
          df.rename(columns={df.columns[0]: 'Timestamp_Str', df.columns[1]: 'Price'}, inplace=True)

          # Extract date and time part before the hyphen and convert to datetime
          df['DateTime'] = df['Timestamp_Str'].apply(
              lambda x: datetime.strptime(x.split('-')[0].strip(), "%d.%m.%Y %H:%M") if '-' in x else None
          )

          # Select only necessary columns
          df_processed = df[['DateTime', 'Price']].copy()

          # Drop rows with NaT in DateTime (if date parsing failed)
          df_processed.dropna(subset=['DateTime'], inplace=True)


          # Group data by year
          if year not in country_data:
            country_data[year] = pd.DataFrame()

          country_data[year] = pd.concat([country_data[year], df_processed], ignore_index=True)


        except Exception as e:
          print(f"      Error processing file {file_name}: {e}")

    # Consolidate and save data for each year for this country without zones
    for year, year_df in country_data.items():
      if not year_df.empty:
        # Sort by DateTime
        year_df.sort_values(by='DateTime', inplace=True)

        # Define the output file path for this country and year
        country_output_path = os.path.join(output_dir, country_folder)
        os.makedirs(country_output_path, exist_ok=True) # Ensure country output directory exists
        output_filepath = os.path.join(country_output_path, f"{year}.csv")

        # Save the resulting DataFrame to a CSV file
        year_df.to_csv(output_filepath, index=False)
        print(f"  Saved processed data for {country_folder} - {year} to {output_filepath}")
      else:
        print(f"  No data processed for {country_folder} - {year}")


print("\nFinished processing all countries in Europe_New.")