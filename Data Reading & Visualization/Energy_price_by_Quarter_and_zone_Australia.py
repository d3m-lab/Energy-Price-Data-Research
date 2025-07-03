import os

df_australia_2020 = pd.read_csv('/content/australia_2020.csv')
df_australia_2020

df_australia_2020_processed = df_australia_2020.melt(id_vars=['SETTLEMENTDATE'], var_name='zone', value_name='price')
df_australia_2020_processed


df_australia_2020_processed['DateTime'] = pd.to_datetime(df_australia_2020_processed['SETTLEMENTDATE'])
df_australia_2020_processed['Quarter'] = df_australia_2020_processed['DateTime'].dt.quarter.apply(lambda x: f'Quarter {x}')

plt.figure(figsize=(12, 8))
g = sns.catplot(data=df_australia_2020_processed, x='Quarter', y='price', hue='zone', kind='bar', height=8, aspect=1.5, palette="Set3")

g.set_axis_labels('Quarter', 'Price (AU$/MWh)', fontsize=22)
#g.fig.suptitle('Australia Energy Price by Quarter (Year 2020)', fontsize=24, y=1.03) # y adjusts the title position

# Adjust font size of x and y ticks
g.set_xticklabels(fontsize=22)
g.set_yticklabels(fontsize=22)

# Set the font size for the legend title
g._legend.set_title('Zone', prop={'size': 20})



# Set the font size for the legend labels
for text in g.legend.get_texts():
    text.set_fontsize(18)

g._legend.set_loc('upper right')
g._legend.set_bbox_to_anchor((0.97, 0.95))

plt.box(True)

plt.grid(True)
plt.tight_layout(rect=[0, 0, 1, 0.98]) # Adjust layout to prevent title overlapping
plt.savefig('australia_energy_price_2020_catplot.eps', format='eps')
plt.show()