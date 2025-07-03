import requests
import zipfile
import io
import pandas as pd
import os

def download_and_extract_nyiso_data(start_year, start_month, end_year, end_month, output_dir="nyiso_data"):
    """
    Downloads NYISO DAM LBMP zone data from a range of dates, extracts,
    and saves each year's data to a separate CSV file.

    Args:
        start_year (int): The starting year (e.g., 2011).
        start_month (int): The starting month (1-12).
        end_year (int): The ending year (e.g., 2025).
        end_month (int): The ending month (1-12).
        output_dir (str): The directory to save the extracted CSV files.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for year in range(start_year, end_year + 1):
        # Initialize a list to hold dataframes for the current year
        yearly_dfs = []

        current_start_month = start_month if year == start_year else 1
        current_end_month = end_month if year == end_year else 12

        for month in range(current_start_month, current_end_month + 1):
            # Construct the URL
            month_str = str(month).zfill(2)
            url = f"https://mis.nyiso.com/public/csv/damlbmp/{year}{month_str}01damlbmp_zone_csv.zip"
            print(f"Attempting to download: {url}")

            try:
                response = requests.get(url)
                response.raise_for_status() # Raise an exception for bad status codes

                # Check if the response content is a zip file
                if response.headers.get('content-type') == 'application/zip':
                    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                        # Assume there's only one file in the zip
                        for file_name in zip_ref.namelist():
                            print(f"Extracting: {file_name}")
                            with zip_ref.open(file_name) as csv_file:
                                df = pd.read_csv(csv_file)
                                yearly_dfs.append(df)
                else:
                    print(f"Warning: URL does not appear to be a zip file: {url}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading {url}: {e}")
                # Continue to the next month/year if download fails

        # Concatenate all dataframes for the current year and save
        if yearly_dfs:
            combined_df = pd.concat(yearly_dfs, ignore_index=True)
            output_filename = os.path.join(output_dir, f"nyiso_{year}.csv")
            combined_df.to_csv(output_filename, index=False)
            print(f"Saved data for year {year} to {output_filename}")
        else:
            print(f"No data downloaded for year {year}.")

# test Example usage:
#download_and_extract_nyiso_data(2024, 1, 2025, 6)
#full download
#download_and_extract_nyiso_data(2011, 1, 2023, 12)