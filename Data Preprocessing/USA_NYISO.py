
import os
import pandas as pd

folder_path = "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Raw/USA/NYISO"

csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
date_column = "Time Stamp"
zone_column = "Name"
price_column = "LBMP ($/MWHr)"

for csv_file in csv_files:
  if csv_files:
    first_csv_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(first_csv_path)
    df_pivot = df.pivot_table(index=date_column, columns=zone_column, values=price_column, aggfunc='first')

    # Reset the index to turn 'date' back into a regular column
    df_pivot = df_pivot.reset_index()

    # Display the transformed DataFrame
    print("\nTransformed DataFrame:")
    print(df_pivot.head())

    output_path = "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Processed/USA/NYISO/"+csv_file
    df_pivot.to_csv(output_path, index=False)
    print(f"\nDataFrame saved to {output_path}")
    #print(df.head())
  else:
    print("No CSV files found in the specified folder.")