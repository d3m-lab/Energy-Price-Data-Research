import os
import pandas as pd
from datetime import datetime
import re
import tqdm
import io

output_directory = r"D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed\Brazil"
os.makedirs(output_directory, exist_ok=True)

# Rename columns
processed_brazil_df = brazil_df.rename(columns={"Hora": "hour", "Submercado": "zone"})

# Melt the DataFrame to transform date columns into rows
processed_brazil_df = processed_brazil_df.melt(id_vars=["hour", "zone"],
                                               var_name="Date",
                                               value_name="Price")
#//processed_brazil_df
processed_brazil_df['Date'] = pd.to_datetime(processed_brazil_df['Date'], errors='coerce')
processed_brazil_df['Date'] = processed_brazil_df['Date'].dt.strftime('%Y-%m-%d')
# Combine 'Date' and 'hour' to create a datetime column
processed_brazil_df['Timestamp'] = pd.to_datetime(processed_brazil_df['Date'].astype(str) + ' ' + processed_brazil_df['hour'].astype(str).str.zfill(2) + ':00:00', format='%Y-%m-%d %H:%M:%S')

# Pivot the DataFrame to make 'zone' columns and 'Datetime' rows
processed_brazil_df = processed_brazil_df.pivot(index='Timestamp', columns='zone', values='Price')

# Reset index to make Datetime a column
processed_brazil_df = processed_brazil_df.reset_index()

# Extract year from the 'Datetime' column
processed_brazil_df['Year'] = processed_brazil_df['Timestamp'].dt.year

# Group by year and save each year to a separate CSV file
for year, year_df in processed_brazil_df.groupby('Year'):
  print("Processing year."+str(year))
  # Drop the 'Year' column before saving
  year_df = year_df.drop(columns=['Year'])
  # Define the output filename
  output_filename = os.path.join(output_directory, f"Brazil_ONS-CCEE_{year}.csv")
  # Save to CSV
  year_df.to_csv(output_filename, index=False)

print("Processing complete and files saved.")
