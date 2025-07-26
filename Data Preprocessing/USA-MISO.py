import os
import pandas as pd
from datetime import datetime

# Define the input and output directories
input_dir = r"D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Raw\USA\MISO"
output_dir = r"D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed\USA\MISO"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Get start and end year from user
start_year = 2011
end_year = 2022

for year in range(start_year, end_year + 1):
    print(f"\nProcessing year: {year}")

    # List all items in the input directory
    items_in_dir = os.listdir(input_dir)

    # Filter for directories starting with the specified year
    target_folders = [item for item in items_in_dir if os.path.isdir(os.path.join(input_dir, item)) and item.startswith(str(year))]

    # Initialize an empty list to store dataframes from each file
    all_dataframes = []

    # Process each target folder
    for folder in target_folders:
        folder_path = os.path.join(input_dir, folder)
        print(f"  Processing folder: {folder_path}")

        # List all files in the current folder
        files_in_folder = os.listdir(folder_path)

        # Filter for .xls files
        xls_files = [file for file in files_in_folder if file.endswith('.xls')]

        # Process each .xls file
        for file_name in xls_files:
            file_path = os.path.join(folder_path, file_name)
            #print(f"    Processing file: {file_path}")

            try:
                # Extract date from the file name
                date_str = file_name[:8]  # e.g., "20180201"
                file_date = datetime.strptime(date_str, '%Y%m%d').date()

                # Read the .xls file, skipping rows before the header and limiting data rows
                df = pd.read_excel(file_path, header=13, nrows=24)
                if ("MISO System" not in df.columns):#logic
                    df = pd.read_excel(file_path, header=14, nrows=24)


                # Rename the first column to 'Hour'
                df.rename(columns={df.columns[0]: 'Hour'}, inplace=True)

                # Add a 'DateTime' column at the beginning
                df.insert(0, 'DateTime', file_date)

                # Process the 'Hour' column
                df['Hour'] = df['Hour'].astype(str)
                df['Hour_Adjusted'] = df['Hour'].apply(lambda x: int(x[-2:]) - 1 if x[-2:].isdigit() else -1)

                # Combine date and hour
                df['DateTime'] = df.apply(
                    lambda row: datetime.combine(row['DateTime'], datetime.min.time()).replace(hour=row['Hour_Adjusted']) if 0 <= row['Hour_Adjusted'] < 24 else None,
                    axis=1
                )
                df = df.rename(columns={"DateTime": "Timestamp"})
                # Drop Hour columns
                df.drop(columns=['Hour', 'Hour_Adjusted'], inplace=True)

                all_dataframes.append(df)

            except Exception as e:
                print(f"    Error processing file {file_name}: {e}")

    # Concatenate all dataframes
    if all_dataframes:
        final_df = pd.concat(all_dataframes, ignore_index=True)

        for col in final_df.columns[1:]:
            try:
                final_df[col] = final_df[col].astype(str)
                final_df[col] = final_df[col].str.replace("'", "")
                final_df[col] = final_df[col].astype(float)
            except Exception as e:
                print(f"    Error processing column {col}: {e}")

        final_df = final_df.sort_values(by=final_df.columns[0])
        output_file_path = os.path.join(output_dir, f"USA_MISO_{year}.csv")
        final_df.to_csv(output_file_path, index=False)
        print(f"  ✅ Saved data for year {year} to {output_file_path}")
    else:
        print(f"  ⚠️ No data found or processed for year {year}")
