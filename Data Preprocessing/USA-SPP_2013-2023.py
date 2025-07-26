import os
import pandas as pd

# Define input and output directories
input_dir = r"D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Raw\USA\SPP_Organized"
output_dir = r"D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed\USA\SPP"

os.makedirs(output_dir, exist_ok=True)

# Valid year range to include
start_year = 2013
end_year = 2023

# Collect all data here
combined_df = pd.DataFrame()

# Get list of year subfolders
year_folders = [folder for folder in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, folder))]

for year_folder in year_folders:
    try:
        year_int = int(year_folder)
    except ValueError:
        print(f"Skipping non-year folder: {year_folder}")
        continue

    if year_int < start_year or year_int > end_year:
        print(f"Skipping out-of-range year: {year_int}")
        continue

    print(f"📁 Processing folder: {year_folder}")
    year_path = os.path.join(input_dir, year_folder)
    csv_files = [f for f in os.listdir(year_path) if f.endswith('.csv')]

    for csv_file in csv_files:
        file_path = os.path.join(year_path, csv_file)
        try:
            df = pd.read_csv(file_path)

            required_columns = ['Interval', 'Settlement Location', 'LMP']
            df = df[required_columns].copy()
            df = df[df['Settlement Location'].isin(["SPPNORTH_HUB", "SPPSOUTH_HUB"])]

            # Pivot data
            df_pivot = df.pivot_table(
                index='Interval',
                columns='Settlement Location',
                values='LMP',
                aggfunc='first'
            )

            df_pivot.index.name = 'Timestamp'
            df_pivot.reset_index(inplace=True)

            # Ensure Timestamp is in datetime format
            df_pivot['Timestamp'] = pd.to_datetime(df_pivot['Timestamp'], format='%m/%d/%Y %I:%M:%S %p',errors='coerce')

            # Drop rows with bad/missing Timestamp
            df_pivot.dropna(subset=['Timestamp'], inplace=True)

            # Add to overall combined dataframe
            combined_df = pd.concat([combined_df, df_pivot], ignore_index=True)

        except Exception as e:
            print(f"⚠️ Error processing file {csv_file}: {e}")

# If data collected, process by year
if not combined_df.empty:
    combined_df['Year'] = combined_df['Timestamp'].dt.year
    combined_df.sort_values(by='Timestamp', inplace=True)

    for year in sorted(combined_df['Year'].unique()):
        year_df = combined_df[combined_df['Year'] == year].drop(columns=['Year'])
        output_filename = f"USA_SPP_{year}.csv"
        output_filepath = os.path.join(output_dir, output_filename)
        year_df.to_csv(output_filepath, index=False)
        print(f"✅ Saved merged data for year {year} to {output_filepath}")
else:
    print("⚠️ No valid data processed.")
