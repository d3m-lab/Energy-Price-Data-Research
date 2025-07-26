
import os
import pandas as pd

folder_path = "E:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Raw\Australia"
output_folder_path ="E:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed\Australia"



csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
date_column = "SETTLEMENTDATE"
zone_column = "REGION"
price_column = "RRP"

for csv_file in csv_files:
  if csv_files:
    first_csv_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(first_csv_path)
    df_pivot = df.pivot_table(index=date_column, columns=zone_column, values=price_column, aggfunc='first')

    # Reset the index to turn 'date' back into a regular column
    df_pivot = df_pivot.reset_index()
    df_pivot = df_pivot.rename(columns={df_pivot.columns[0]: "Timestamp"})
    df_pivot = df_pivot.sort_values(by='Timestamp')


    year_match = re.search(r'_(\d{4})\.', csv_file)
    if year_match:
        year = year_match.group(1)
        #print(year)
    else:
        print("Year not found in filename.")

    new_file_name = "AUSTRALIA_AEMO_"+ year + ".csv"
    #print(new_file_name)
    # Display the transformed DataFrame
    print("\nTransformed DataFrame:")
    print(df_pivot.head())
    output_path = output_folder_path+ '\\' + new_file_name
    df_pivot.to_csv(output_path, index=False)
    print(f"\nDataFrame saved to {output_path}")
    #print(df.head())
  else:
    print("No CSV files found in the specified folder.")