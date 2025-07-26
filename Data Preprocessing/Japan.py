import os
import pandas as pd

def process_and_save_japan_data(start_year, end_year, input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Define new headers
    new_headers = [
        'Date', 'Hour', 'Info 1', 'Info 2', 'Info 3', 'System Price',
        'Hokkaido', 'Tohoku', 'Tokyo', 'Chubu', 'Hokuriko', 'Kansai',
        'Chugoku', 'Shikoku', 'Kyushu', 'Info 5', 'Info 6', 'Info 7', 'Info 8'
    ]

    # Define columns to keep
    output_columns = [
        'Timestamp', 'System Price', 'Hokkaido', 'Tohoku', 'Tokyo',
        'Chubu', 'Hokuriko', 'Kansai', 'Chugoku', 'Shikoku', 'Kyushu'
    ]

    # Combine all processed data into this DataFrame
    combined_df = pd.DataFrame()

    for year in range(start_year, end_year + 1):
        file_name = f"spot_summary_{year}.csv"
        file_path = os.path.join(input_dir, file_name)

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path, encoding='shift_jis')

                # Rename columns
                if df.shape[1] >= len(new_headers):
                    df = df.iloc[:, :len(new_headers)]
                    df.columns = new_headers
                else:
                    print(f"Skipping {file_name} due to unexpected column count.")
                    continue

                # Parse Timestamp
                df['Date_dt'] = pd.to_datetime(df['Date'], errors='coerce')
                df['Hour_adj'] = (df['Hour'] - 1).astype(int)
                df['Timestamp'] = df.apply(lambda row: row['Date_dt'] + pd.Timedelta(minutes=30 * row['Hour_adj']), axis=1)

                # Filter necessary columns
                df_clean = df[output_columns].copy()

                # Append to combined
                combined_df = pd.concat([combined_df, df_clean], ignore_index=True)

                print(f"Read and processed: {file_name}")

            except Exception as e:
                print(f"Error processing {file_name}: {e}")
        else:
            print(f"File not found: {file_path}")

    # Drop rows with invalid timestamps
    combined_df.dropna(subset=['Timestamp'], inplace=True)

    # Extract year from Timestamp and save by year
    combined_df['Year'] = combined_df['Timestamp'].dt.year

    for year in sorted(combined_df['Year'].unique()):
        year_df = combined_df[combined_df['Year'] == year].drop(columns=['Year'])
        output_file_name = f"Japan_JEPX_{year}.csv"
        output_file_path = os.path.join(output_dir, output_file_name)
        year_df.to_csv(output_file_path, index=False)
        print(f"Saved data for year {year} to {output_file_path}")

# Define directories
input_directory = r"D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Raw\Japan"
output_directory = r"D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed\Japan"

# Get year range from user
while True:
    try:
        start_year_input = int(input("Enter the start year (e.g., 2005): "))
        end_year_input = int(input("Enter the end year (e.g., 2022): "))
        if start_year_input <= end_year_input:
            break
        else:
            print("Start year must be less than or equal to end year.")
    except ValueError:
        print("Invalid input. Please enter valid years.")

# Run processing
process_and_save_japan_data(start_year_input, end_year_input, input_directory, output_directory)
