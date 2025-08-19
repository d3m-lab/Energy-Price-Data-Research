import pandas as pd
import pytz

# Assuming 'df' is already loaded with the timestamp data
# Assuming 'offsets' is already loaded with the offset data
file_path = r"D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed\USA\NYISO\USA_NYISO_2024.csv"
offset_file_path = r"D:\OneDrive - The Pennsylvania State University\Research DATA\Dr. Habib & Dr. Reza Data\Energy Price Market Data\Day Ahead Price Data_Processed\Price_Unit_by_Country_with_offset.csv"
df = pd.read_csv(file_path)
offsets = pd.read_csv(offset_file_path)

# Define country and market for the current dataset
country = "USA"
market = "NYISO"

# Find the timezone name for the given country and market
tz_name = country_market_tz.get((country, market))

# Convert 'Timestamp' to datetime objects if not already
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Convert to UTC
if tz_name:
    try:
        tz = pytz.timezone(tz_name)
        # Localize the timestamp to the specific timezone, handling ambiguous and nonexistent times
        df["Timestamp_UTC"] = df["Timestamp"].dt.tz_localize(tz, ambiguous="NaT", nonexistent="NaT").dt.tz_convert("UTC")
        print("Timestamp converted to UTC successfully.")
    except pytz.UnknownTimeZoneError:
        df["Timestamp_UTC"] = None
        print(f"Error: Unknown timezone '{tz_name}'")
else:
    df["Timestamp_UTC"] = None
    print(f"Could not find timezone for {country} - {market} combination.")

# Convert Timestamp_UTC to ISO format string (without timezone offset)
if "Timestamp_UTC" in df.columns and df["Timestamp_UTC"].notna().any():
    df["Timestamp_UTC"] = df["Timestamp_UTC"].dt.strftime('%Y-%m-%dT%H:%M:%S')
    df["Timestamp"] = df["Timestamp"].dt.strftime('%Y-%m-%dT%H:%M:%S')

# Reorder columns so Timestamp_UTC is first
cols = ["Timestamp_UTC"] + [col for col in df.columns if col != "Timestamp_UTC"]
df = df[cols]

# Display the DataFrame with the new UTC timestamp column in ISO format
display(df.head())