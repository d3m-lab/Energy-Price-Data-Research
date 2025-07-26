

# Define the input and output directories
input_dir = r"D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Raw\USA\CAISO_New_07.14.2025"
output_dir = r"D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed\USA\CAISO_NEW"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define the columns to keep and their new names
selected_columns = {
    "Local Timestamp Pacific Time (Interval Beginning)": "Timestamp",
    "NP-15 LMP": "TH_NP15_GEN-APND",
    "SP-15 LMP": "TH_SP15_GEN-APND",
    "ZP-26 LMP": "TH_ZP26_GEN-APND"
}

# Iterate through each file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_dir, filename)
        print(f"Processing file: {filename}")

        try:
            # Read the CSV file, skipping the first 3 rows (header is row 4)
            # and reading data from row 5 onwards
            df = pd.read_csv(file_path, header=3)

            # Ensure the required columns exist in the DataFrame
            if all(col in df.columns for col in selected_columns.keys()):

                # Select and rename the columns
                df_processed = df[list(selected_columns.keys())].rename(columns=selected_columns)

                # Combine "Timestamp" and "Hour Number" to create a datetime timestamp
                # Assuming 'Timestamp' column contains the date and 'Hour Number' contains the hour (1-24)
                # We need to combine them and adjust the hour for datetime object (0-23)
                # The original 'Local Timestamp Pacific Time (Interval Beginning)' already includes date and time,
                # so we just need to ensure it's in datetime format.
                # Let's confirm the format of 'Local Timestamp Pacific Time (Interval Beginning)'
                # If it's already a full timestamp string, we just convert it.
                # If 'Hour Number' is truly needed, we would combine it with the date part of 'Local Timestamp'.
                # Given the column name "Local Timestamp Pacific Time (Interval Beginning)", it's highly likely
                # it contains the full timestamp. We just need to convert it to datetime objects.
                df_processed['Timestamp'] = pd.to_datetime(df_processed['Timestamp'], errors='coerce')

                # Drop rows where Timestamp could not be created
                df_processed.dropna(subset=['Timestamp'], inplace=True)

                # Set 'Timestamp' as the index and sort
                df_processed.set_index('Timestamp', inplace=True)
                df_processed.sort_index(inplace=True)

                # Extract the year from the filename
                match = re.search(r'\d{4}', filename)
                if match:
                    year = match.group(0)
                else:
                    print(f"Could not extract year from filename: {filename}. Skipping.")
                    continue

                # Define the output filename and path
                output_filename = f"USA_CAISO_{year}.csv"
                output_filepath = os.path.join(output_dir, output_filename)

                # Save the processed dataframe
                df_processed.to_csv(output_filepath)
                print(f"✅ Processed and saved {filename} to {output_filepath}")

            else:
                missing_cols = [col for col in selected_columns.keys() if col not in df.columns]
                print(f"Skipping file {filename}: Missing required columns: {missing_cols}")

        except Exception as e:
            print(f"Error processing file {filename}: {e}")

print("\nCAISO NEW data preprocessing complete.")
