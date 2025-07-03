

file_path = r"E:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed\USA\NYISO\USA_NYISO_2024.csv"
df = pd.read_csv(file_path)
df



# Check if 'Timestamp' and 'CAPITL' columns exist
if 'Timestamp' in df.columns and 'CAPITL' in df.columns:
    # Convert 'Timestamp' to datetime objects
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Sort data by Timestamp to ensure proper line plot
    df = df.sort_values('Timestamp')

    # Create the line chart
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='Timestamp', y='CAPITL', data=df)
    plt.title('CAPITL over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('CAPITL')
    plt.xticks(rotation=45) # Rotate x-axis labels for better readability
    plt.tight_layout() # Adjust layout
    plt.show()
else:
    print("The DataFrame must contain 'Timestamp' and 'CAPITL' columns for this visualization.")
