import os
import pandas as pd
from datetime import datetime
import re
import tqdm
import io


# Define source and destination directories
source_directory = 'D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Raw\South Korea'
destination_directory = 'D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed\South Korea'

# Create the destination directory if it doesn't exist
os.makedirs(destination_directory, exist_ok=True)

# List all files in the source directory
all_files = os.listdir(source_directory)

# Filter for CSV files that match the pattern HourlySMP_{zone}.csv
csv_files = [f for f in all_files if f.startswith('HourlySMP_') and f.endswith('.csv')]

# Initialize an empty dictionary to store processed dataframes by zone
processed_dataframes = {}

# Process each CSV file
for csv_file in csv_files:
    file_path = os.path.join(source_directory, csv_file)
    # Extract the zone name from the filename
    match = re.match(r'HourlySMP_(.*)\.csv', csv_file)
    if match:
        zone = match.group(1)
        print(f"Processing file: {csv_file} for zone: {zone}")

        # Read the CSV file
        df = pd.read_csv(file_path)
        # Drop specific columns if they exist
        columns_to_drop = ['Max', 'Min', 'Weighted']
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

        # Ensure the 'Period' column is treated as datetime
        df['Period'] = pd.to_datetime(df['Period'])

        # Melt the dataframe to transform hourly columns into rows
        # Identify hour columns (those that are not 'Period')
        #hour_columns = [col for col in df.columns if col != 'Period']
        hour_columns = [col for col in df.columns if re.match(r'^\d{2} h$', col.strip())]
        melted_df = df.melt(id_vars='Period', value_vars=hour_columns, var_name='Hour', value_name=zone)

        # Convert 'Hour' column to extract the hour number
        melted_df['Hour_Num'] = melted_df['Hour'].apply(lambda x: int(x.split()[0]))

        # Combine 'Period' (date) and 'Hour_Num' to create a datetime index
        # Use .apply with lambda to create datetime objects correctly
        melted_df['Timestamp'] = melted_df.apply(
            lambda row: row['Period'] + pd.Timedelta(hours=row['Hour_Num'] - 1), axis=1
        )

        # Keep only the relevant columns: DateTime and the zone value column
        processed_df = melted_df[['Timestamp', zone]].set_index('Timestamp')

        # Store the processed dataframe for this zone
        processed_dataframes[zone] = processed_df

# Combine all processed dataframes based on the DateTime index
if processed_dataframes:
    # Start with the first processed dataframe
    combined_df = list(processed_dataframes.values())[0]

    # Join with the remaining dataframes
    for zone, df in list(processed_dataframes.items())[1:]:
        combined_df = combined_df.join(df, how='outer') # Use 'outer' join to keep all date/time combinations

    # Rename the index to 'DateTime' (optional, as it's already the index name)
    combined_df.index.name = 'Timestamp'

    # Sort the combined dataframe by DateTime
    combined_df.sort_index(inplace=True)

    # Extract year from the index
    combined_df['Year'] = combined_df.index.year

    # Save the combined dataframe by year
    for year, year_df in combined_df.groupby('Year'):
        output_filename = f'South Korea_KPX_{year}.csv'
        output_filepath = os.path.join(destination_directory, output_filename)
        # Drop the 'Year' column before saving
        year_df = year_df.drop(columns=['Year'])
        if year <= 2009:
          year_df = year_df.drop(columns=['Jeju'], errors='ignore')
        year_df.to_csv(output_filepath)
        print(f"Saved data for year {year} to {output_filepath}")
else:
    print("No CSV files found matching the pattern in the source directory.")

