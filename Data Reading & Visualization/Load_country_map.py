import geopy
from geopy.geocoders import Nominatim
import folium

# Replace this with the actual path to your folder in Google Drive
base_folder = 'E:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed'

country_list = []

# Walk through the directory and its subdirectories
for root, dirs, files in os.walk(base_folder):
    for name in dirs:
        # Assuming each subdirectory name is a country name
        country_list.append(name)

# Remove duplicates and sort for better organization
country_list = sorted(list(set(country_list)))

print("Identified Countries:")
print(country_list)

# Get latitude and longitude for each country
geolocator = Nominatim(user_agent="country_mapper")
country_coords = {}

for country in country_list:
    try:
        location = geolocator.geocode(country)
        if location:
            country_coords[country] = (location.latitude, location.longitude)
            print(f"Found coordinates for {country}: {location.latitude}, {location.longitude}")
        else:
            print(f"Could not find coordinates for {country}")
    except Exception as e:
        print(f"Error finding coordinates for {country}: {e}")


# Create a world map
world_map = folium.Map(location=[0, 0], zoom_start=2) # Center the map

# Add markers for each country
for country, coords in country_coords.items():
    folium.Marker(
        location=coords,
        popup=country,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(world_map)

# Display the map (in Colab this will render an interactive map)
display(world_map)
