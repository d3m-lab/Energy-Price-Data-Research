

import os
import pandas as pd

folder_path = "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Raw/USA/ERCOT"

csv_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
date_column = "Datetime"
zone_column = "Settlement Point"
price_column = "Settlement Point Price"

for csv_file in csv_files:
  if csv_files:
    file_name, file_extension = os.path.splitext(csv_file)


    first_csv_path = os.path.join(folder_path, csv_file)
    df = pd.read_excel(first_csv_path)
    # --- Start of Added Code ---
    # Handle '24:00' in 'Hour Ending' by converting to '00:00' and adding one day
    mask_24 = df['Hour Ending'] == '24:00'
    df.loc[mask_24, 'Hour Ending'] = '00:00'
    # Convert 'Delivery Date' to datetime temporarily to add a day
    df['Delivery Date'] = pd.to_datetime(df['Delivery Date'], format='%m/%d/%Y')
    df.loc[mask_24, 'Delivery Date'] = df.loc[mask_24, 'Delivery Date'] + pd.Timedelta(days=1)
    # Convert 'Delivery Date' back to string if needed later, although converting to datetime is the goal
    # For the next step, it's better to keep it as datetime
    # --- End of Added Code ---

    # Convert 'Delivery Date' (which is now datetime) to string in '%Y-%m-%d' format
    date_str = df['Delivery Date'].dt.strftime('%Y-%m-%d')

    # Combine the date string and hour string
    datetime_str = date_str + ' ' + df['Hour Ending']

    # Convert the combined string to datetime
    df['Datetime'] = pd.to_datetime(datetime_str, format='%Y-%m-%d %H:%M')


    df_pivot = df.pivot_table(index=date_column, columns=zone_column, values=price_column, aggfunc='first')

    # Reset the index to turn 'date' back into a regular column
    df_pivot = df_pivot.reset_index()

    # Display the transformed DataFrame
    print("\nTransformed DataFrame:")
    print(df_pivot.head())

    output_path = "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Processed/USA/ERCOT/"+file_name+".csv"
    df_pivot.to_csv(output_path, index=False)
    print(f"\nDataFrame saved to {output_path}")
    #print(df.head())
  else:
    print("No CSV files found in the specified folder.")