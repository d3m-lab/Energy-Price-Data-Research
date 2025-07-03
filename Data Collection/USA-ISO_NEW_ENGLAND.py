import os
import pandas as pd
from datetime import datetime
import re

def download_and_process_isone_data(start_year, start_month, start_day, end_year, end_month, end_day):
    """
    Downloads, processes, and saves ISO New England Day-Ahead LMP data for a specified date range.

    Args:
        start_year (int): The starting year.
        start_month (int): The starting month (1-12).
        start_day (int): The starting day (1-31).
        end_year (int): The ending year.
        end_month (int): The ending month (1-12).
        end_day (int): The ending day (1-31).
    """
    base_url = "https://www.iso-ne.com/static-transform/csv/histRpts/da-lmp/WW_DALMP_ISO_{year}{month:02d}{day:02d}.csv"
    output_base_path = "/content/drive/MyDrive/Research/Dr. Habib & Dr. Reza Data/Energy Price Market Data/Day Ahead Price Data_Raw/USA/ISO_NEW_ENGLAND"
    os.makedirs(output_base_path, exist_ok=True)

    start_date = pd.to_datetime(f'{start_year}-{start_month}-{start_day}')
    end_date = pd.to_datetime(f'{end_year}-{end_month}-{end_day}')

    current_date = start_date

    # Dictionary to store combined dataframes per year
    yearly_dataframes = {}

    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        day = current_date.day

        url = base_url.format(year=year, month=month, day=day)
        print(f"Attempting to download: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            # Read the CSV content into a DataFrame
            # Header is 4 (0-indexed), so use header=3
            # Skip row 5 (0-indexed), so use skiprows=[4]
            df = pd.read_csv(io.StringIO(response.text), header=4, skiprows=[5], low_memory=False)

            # Filter rows where 'Location Name' starts with '.Z.'
            df_filtered = df[df['Location Name'].fillna('').str.startswith('.Z.')].copy()

            df_filtered['Hour'] = pd.to_numeric(df_filtered['Hour Ending'], errors='coerce') - 1

            # Drop rows where 'Hour' is NaN after coercion
            df_filtered.dropna(subset=['Hour'], inplace=True)

            # Convert 'Hour' to integer after removing NaNs
            df_filtered['Hour'] = df_filtered['Hour'].astype(int)


            # Create Datetime column
            # Format 'Date' as MM/DD/YYYY
            df_filtered['Date_Formatted'] = pd.to_datetime(df_filtered['Date']).dt.strftime('%m/%d/%Y')

            df_filtered['Datetime'] = pd.to_datetime(df_filtered['Date_Formatted'] + ' ' + df_filtered['Hour'].astype(str) + ':00', format='%m/%d/%Y %H:%M')

            # Select required columns and rename
            df_processed = df_filtered[['Datetime', 'Location Name', 'Locational Marginal Price']].copy()
            df_processed.rename(columns={'Locational Marginal Price': 'Price'}, inplace=True)

            # Pivot the data to have 'Datetime' as index and 'Location Name' as columns
            #df_pivot = df_processed.pivot_table(index='Datetime', columns='Location Name', values='Price')

            # Append to the yearly dataframes dictionary
            if year not in yearly_dataframes:
                yearly_dataframes[year] = []
            yearly_dataframes[year].append(df_processed)

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
        #except Exception as e:
        #    print(f"Error processing data from {url}: {e}")

        # Move to the next day
        current_date += pd.Timedelta(days=1)
        # Add a small delay to avoid hammering the server
        #time.sleep(0.5)


    # After the loop, combine and save data for each year
    for year, list_of_dfs in yearly_dataframes.items():
        if list_of_dfs:
            combined_year_df = pd.concat(list_of_dfs).sort_index()
            # Ensure index is unique before saving
            #combined_year_df = combined_year_df[~combined_year_df.index.duplicated(keep='first')]
            combined_year_df = combined_year_df.sort_index()
            combined_year_df = combined_year_df.sort_values(by='Datetime')
            #combined_year_df = combined_year_df.set_index('Datetime')
            output_file_path = os.path.join(output_base_path, f'{year}.csv')
            combined_year_df.to_csv(output_file_path,index=False)
            print(f"Saved combined and processed data for year {year} to: {output_file_path}")
        else:
            print(f"No data processed for year {year}.")


# Example usage: Download and process data for 2024
download_and_process_isone_data(2018, 6, 11, 2025, 5, 31)