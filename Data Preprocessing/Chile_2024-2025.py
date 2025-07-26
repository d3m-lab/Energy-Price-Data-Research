import os
import pandas as pd
from datetime import datetime
import re
import tqdm
import io

year = input("Enter the year: ")
year_str = str(year)
input_filename = f"{year_str}.xlsx"
output_filename = f"Chile_CEN_{year_str}.csv"
input_filepath = os.path.join("D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Raw\Chile_PreProcessed", input_filename)
output_filepath = os.path.join("D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed\Chile", output_filename)
# Check if the input file exists
if not os.path.exists(input_filepath):
    print(f"Error: Input file not found at {input_filepath}")
else:
    try:
        # Read the CSV file
        df_year = pd.read_excel(input_filepath)


        # Ensure necessary columns exist
        if 'Fecha' not in df_year.columns or 'Hora' not in df_year.columns:
            print(f"Skipping processing for {year_str}: Missing 'Fecha' or 'Hora' column.")
        else:
            # Combine 'Fecha' and 'Hora' into a Timestamp column
            # Assuming 'Fecha' is in 'YYYY-MM-DD' format and 'Hora' is integer hour (0-23)
            df_year['Timestamp'] = pd.to_datetime((df_year['Fecha']).astype(str) + ' ' + (df_year['Hora']).astype(str) + ':00:00', errors='coerce')
            # Drop rows where Timestamp could not be created
            df_year.dropna(subset=['Timestamp'], inplace=True)
            # Remove 'Dia' and 'Barra' columns if they exist
            columns_to_drop = ['Dia', 'Barra', 'Fecha', 'Hora']
            df_year = df_year.drop(columns=[col for col in columns_to_drop if col in df_year.columns])
            # Set Timestamp as index
            df_year.set_index('Timestamp', inplace=True)
            #print(df_year);
            #exitlsdas;
            # Check if the output file exists
            if os.path.exists(output_filepath):
                print(f"Output file already exists at {output_filepath}. Reading existing data.")
                try:
                    existing_df = pd.read_csv(output_filepath, index_col='Timestamp', parse_dates=True)

                    # Update existing DataFrame with new data, matching by Timestamp index
                    # This will replace rows in existing_df with matching indices from df_year
                    # If index is not present in existing_df, it will be added
                    existing_df.update(df_year)
                    # If you want to add new rows from df_year that are not in existing_df
                    # You can use combine_first
                    df_to_save = existing_df.combine_first(df_year)
                    print("Existing file updated.")
                except Exception as e:
                    print(f"Error reading or updating existing file: {e}. Saving new data.")
                    df_to_save = df_year
            else:
                df_to_save = df_year
            # Save the processed dataframe
            df_to_save.to_csv(output_filepath)
            print(f"Processed data for year {year_str} saved to {output_filepath}")
    except Exception as e:
        print(f"Error processing input file for year {year_str}: {e}")