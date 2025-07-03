import pandas as pd

df_2020 = pd.read_csv('/content/India/2020.csv')
df_2020


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Convert 'DateTime' to datetime objects
df_2020['DateTime'] = pd.to_datetime(df_2020['DateTime'])

# Extract month name
df_2020['Month'] = df_2020['DateTime'].dt.month_name()


# Create a mapping for month names to abbreviations
month_abbr_map = {
    'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr',
    'May': 'May', 'June': 'Jun', 'July': 'Jul', 'August': 'Aug',
    'September': 'Sep', 'October': 'Oct', 'November': 'Nov', 'December': 'Dec'
}

# Apply the mapping to the 'Month' column
df_2020['Month_Abbr'] = df_2020['Month'].map(month_abbr_map)

# Drop the original 'Month' column
df_2020 = df_2020.drop('Month', axis=1)


# Define the order of months for plotting
month_order = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]

plt.figure(figsize=(12, 8)) # Adjust figure size as needed
sns.violinplot(data=df_2020, x='Month_Abbr', y='Price (Rs./MWh)', order=month_order, linewidth=1, palette="Set3")

plt.xlabel('Month', fontsize=24)
plt.ylabel('Price (Rs./MWh)', fontsize=24)
#plt.title('India Energy Price by Month (Year 2020)', fontsize=18)

plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.grid(True)
plt.tight_layout() # Adjust layout to prevent labels overlapping
plt.savefig('india_energy_price_2020_violin.eps', format='eps')
plt.show()