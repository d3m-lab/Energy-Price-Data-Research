import os
import pandas as pd

# Define directories
input_dir = r"D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Raw\USA\SPP_Organized"
output_dir = r"D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data_Processed\USA\SPP"

# Ensure output path exists
os.makedirs(output_dir, exist_ok=True)

# Years you want to process
years_to_process = [2024, 2025]

# Collect all valid pivoted dataframes
all_data = []

for year in years_to_process:
    print(f"\n🔄 Processing folder: {year}")
    year_path = os.path.join(input_dir, str(year))

    if not os.path.exists(year_path):
        print(f"  ⚠️ Folder not found: {year_path}")
        continue

    csv_files = [f for f in os.listdir(year_path) if f.endswith('.csv')]
    if not csv_files:
        print(f"  ⚠️ No CSV files in {year_path}")
        continue

    for file_name in csv_files:
        file_path = os.path.join(year_path, file_name)

        try:
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip()

            # Drop unwanted column
            df = df.drop(columns=['PNODE Name'], errors='ignore')

            # Identify HE columns
            he_columns = [col for col in df.columns if col.startswith('HE')]

            # Melt the data
            df_melted = df.melt(
                id_vars=[col for col in df.columns if col not in he_columns],
                value_vars=he_columns,
                var_name='Hour_HE',
                value_name='Price_Value'
            )

            # Extract hour and compute Timestamp
            df_melted['Hour'] = df_melted['Hour_HE'].str.extract(r'HE(\d{2})').astype(int) - 1
            df_melted['Timestamp'] = pd.to_datetime(
                df_melted['Date'] + ' ' + df_melted['Hour'].astype(str) + ':00:00',
                errors='coerce'
            )

            # Clean up
            df_melted = df_melted.drop(columns=['Hour_HE', 'Hour', 'Date'])
            df_melted.rename(columns={'Price_Value': 'LMP'}, inplace=True)

            # Filter by hub and price type
            df_filtered = df_melted[
                (df_melted['Settlement Location Name'].isin(["SPPNORTH_HUB", "SPPSOUTH_HUB"])) &
                (df_melted['Price Type'] == "LMP")
            ].copy()

            df_filtered.drop(columns=['Price Type'], inplace=True)

            # Pivot
            df_final = df_filtered.pivot_table(
                index='Timestamp',
                columns='Settlement Location Name',
                values='LMP',
                aggfunc='first'
            )


            all_data.append(df_final)

        except Exception as e:
            print(f"  ❌ Error in {file_name}: {e}")

# Merge all data across years
if all_data:
    combined_df = pd.concat(all_data).sort_index()
    combined_df = combined_df.reset_index()
    combined_df['Timestamp'] = pd.to_datetime(combined_df['Timestamp'], format='%m/%d/%Y %I:%M:%S %p',  errors='coerce')
    combined_df.dropna(subset=['Timestamp'], inplace=True)
    combined_df.sort_values(by='Timestamp', inplace=True)

    # Extract year from Timestamp
    combined_df['Year'] = combined_df['Timestamp'].dt.year

    # Save by year
    for year in sorted(combined_df['Year'].unique()):
        df_year = combined_df[combined_df['Year'] == year].drop(columns=['Year'])
        df_year = df_year.set_index('Timestamp')

        output_file = os.path.join(output_dir, f"USA_SPP_{year}.csv")
        df_year.to_csv(output_file)
        print(f"✅ Saved: {output_file}")
else:
    print("⚠️ No valid data was processed.")
