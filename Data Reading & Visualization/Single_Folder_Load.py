
folder_path = r"E:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed\USA\NYISO"

csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Assuming you want to read the first CSV file found in the folder
if csv_files:
    first_csv_file_path = os.path.join(folder_path, csv_files[0])
    df = pd.read_csv(first_csv_file_path)
    print(df)
else:
    print("No CSV files found in the specified folder.")