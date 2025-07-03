nyiso_path = '/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Processed/USA/NYISO'
csv_files = [f for f in os.listdir(nyiso_path) if f.endswith('.csv') and 'nyiso_2025.csv' not in f]

all_nyiso_data = pd.DataFrame()

for file in csv_files:
    file_path = os.path.join(nyiso_path, file)
    df = pd.read_csv(file_path)
    all_nyiso_data = pd.concat([all_nyiso_data, df], ignore_index=True)

all_nyiso_data


all_nyiso_data['Time Stamp'] = pd.to_datetime(all_nyiso_data['Time Stamp'])
all_nyiso_data['Year'] = all_nyiso_data['Time Stamp'].dt.year
all_nyiso_data['Month'] = all_nyiso_data['Time Stamp'].dt.month_name()
all_nyiso_data



frame = all_nyiso_data.copy()

# Reorder months for the heatmap
month_order_heatmap = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Pivot the dataframe for the heatmap
heatmap_data = frame.pivot_table(values='CAPITL', index='Month', columns='Year', aggfunc='mean')
heatmap_data = heatmap_data.reindex(month_order_heatmap) # Ensure months are in order

plt.figure(figsize=(14, 10))
sns.heatmap(heatmap_data, annot=True, linewidths=.5, cmap="Set3")

plt.title('Price ($/MWh)', fontsize=16)
plt.xlabel('Year', fontsize=16)
plt.ylabel('Month', fontsize=16)

plt.xticks(fontsize=14, rotation=45, ha='right')
plt.yticks(fontsize=14)

plt.tight_layout()
plt.savefig('new_york_energy_price_heatmap.eps', format='eps')
plt.show()
