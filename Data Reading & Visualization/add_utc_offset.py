import pandas as pd
import pytz

# Read your CSV
df = pd.read_csv(file_path)

# Country + Market → Timezone mapping
country_market_tz = {
    ("India", "IEX"): "Asia/Kolkata",
    ("Japan", "JEPX"): "Asia/Tokyo",
    ("Singapore", "NEMS"): "Asia/Singapore",
    ("South Korea", "KPX"): "Asia/Seoul",
    ("Austria", "EPEX SPOT, Nord Pool"): "Europe/Vienna",
    ("Belgium", "EPEX SPOT, Nord Pool"): "Europe/Brussels",
    ("Denmark", "EPEX SPOT, Nord Pool"): "Europe/Copenhagen",
    ("Finland", "EPEX SPOT, Nord Pool"): "Europe/Helsinki",
    ("France", "EPEX SPOT, Nord Pool"): "Europe/Paris",
    ("Germany", "EPEX SPOT, Nord Pool"): "Europe/Berlin",
    ("Netherlands", "EPEX SPOT, Nord Pool"): "Europe/Amsterdam",
    ("Norway", "EPEX SPOT, Nord Pool"): "Europe/Oslo",
    ("Poland", "EPEX SPOT, Nord Pool"): "Europe/Warsaw",
    ("Sweden", "EPEX SPOT, Nord Pool"): "Europe/Stockholm",
    ("Luxembourg", "EPEX SPOT"): "Europe/Luxembourg",
    ("Switzerland", "EPEX SPOT"): "Europe/Zurich",
    ("Estonia", "Nord Pool"): "Europe/Tallinn",
    ("Latvia", "Nord Pool"): "Europe/Riga",
    ("Lithuania", "Nord Pool"): "Europe/Vilnius",
    ("Croatia", "CROPEX"): "Europe/Zagreb",
    ("Czech Republic", "OTE"): "Europe/Prague",
    ("Greece", "HEnEx"): "Europe/Athens",
    ("Hungary", "HUPX"): "Europe/Budapest",
    ("Ireland", "SEMOpx"): "Europe/Dublin",
    ("Italy", "IPEX"): "Europe/Rome",
    ("Montenegro", "MEPX"): "Europe/Podgorica",
    ("North Macedonia", "MEMO"): "Europe/Skopje",
    ("Portugal", "MIBEL"): "Europe/Lisbon",
    ("Spain", "MIBEL"): "Europe/Madrid",
    ("Serbia", "SEEPEX"): "Europe/Belgrade",
    ("Slovakia", "OKTE"): "Europe/Bratislava",
    ("Slovenia", "BSP"): "Europe/Ljubljana",
    ("United Kingdom", "EPEX SPOT"): "Europe/London",
    ("Canada", "IESO"): "America/Toronto",
    ("Australia", "AEMO"): "Australia/Sydney",
    ("Brazil", "CCEE"): "America/Sao_Paulo",
    ("Chile", "CEN"): "America/Santiago",
    ("Bulgaria", "IBEX"): "Europe/Sofia",
    ("Romania", "OPCOM"): "Europe/Bucharest",

    # U.S. markets explicitly
    ("USA", "CAISO"): "America/Los_Angeles",     # Pacific
    ("USA", "ERCOT"): "America/Chicago",         # Central
    ("USA", "NEW ENGLAND"): "America/New_York",  # Eastern
    ("USA", "MISO"): "America/Chicago",          # Central
    ("USA", "NYISO"): "America/New_York",        # Eastern
    ("USA", "PJM"): "America/New_York",          # Eastern
    ("USA", "SPP"): "America/Chicago",           # Central
}

# Function to compute UTC offset in HH:MM
def get_offset(row):
    tz_name = country_market_tz.get((row["Country"], row["Market"]))
    if not tz_name:
        return None
    tz = pytz.timezone(tz_name)
    
    # Take start timestamp
    start_str = row["Start Timestamp - End Timestamp"].split(" - ")[0]
    start_dt = pd.to_datetime(start_str)
    
    # Localize
    local_dt = tz.localize(start_dt, is_dst=None)
    offset = local_dt.utcoffset()
    
    # Format HH:MM
    total_minutes = int(offset.total_seconds() / 60)
    hours, minutes = divmod(abs(total_minutes), 60)
    sign = "+" if total_minutes >= 0 else "-"
    return f"{sign}{hours:02d}:{minutes:02d}"

# Add UTC Offset column
df["UTC Offset"] = df.apply(get_offset, axis=1)

# Save new CSV
df.to_csv(offset_file_path, index=False)
print("✅ New CSV saved as "+offset_file_path)
