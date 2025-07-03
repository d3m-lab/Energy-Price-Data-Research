import os
import pandas as pd
df_norway_2020 = pd.read_csv('/content/Norway/2020.csv')
df_norway_2020


df_norway_2020_processed = df_norway_2020.melt(id_vars=['DateTime'], var_name='zone', value_name='price')

# Convert 'DateTime' to datetime objects and extract the date
df_norway_2020_processed['DateTime'] = pd.to_datetime(df_norway_2020_processed['DateTime'])
df_norway_2020_processed['Date'] = df_norway_2020_processed['DateTime'].dt.date

# Calculate the mean price for each date and zone
df_norway_daily_mean = df_norway_2020_processed.groupby(['Date', 'zone'])['price'].mean().reset_index()

# Display the resulting DataFrame
df_norway_daily_mean



df_norway_2020_processed['Date'] = pd.to_datetime(df_norway_2020_processed['Date'])

plt.figure(figsize=(16, 8)) # Adjust figure size as needed
g= sns.lineplot(data=df_norway_2020_processed, x='Date', y='price', hue='zone')

plt.xlabel('Date', fontsize=24)
plt.ylabel('Price (€/MWh)', fontsize=24)
#plt.title('Norway Energy Price (Year 2020)', fontsize=24)

plt.xticks(fontsize=22)
plt.yticks(fontsize=22)


# Set the font size for the legend title
g.legend_.set_title('Zone', prop={'size': 20})
# Set the font size for the legend labels
for text in g.legend_.get_texts():
    text.set_fontsize(18)

g.legend_.set_loc('upper left')
#g.legend_.set_bbox_to_anchor((0.97, 0.95))


plt.tight_layout(rect=[0, 0, 1, 0.98]) # Adjust layout to prevent labels overlapping

plt.grid(True)

plt.savefig('norway_energy_price_2020_line.eps', format='eps')
plt.show()
