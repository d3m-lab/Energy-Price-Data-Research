
import pandas as pd
import requests # Import the requests library
import io # Import the io library to read the response content

url = "https://www.aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_202401_NSW1.csv"

# Define a user-agent to mimic a web browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    # Use requests to get the content with headers
    response = requests.get(url, headers=headers)
    response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

    # Read the content into a pandas DataFrame
    # We need to read the text content from the response
    df = pd.read_csv(io.StringIO(response.text))
    print("Successfully downloaded and read the DataFrame:")
    display(df) # Use display for better formatting in notebooks

except requests.exceptions.RequestException as e:
    print(f"Error downloading data: {e}")
    print("Please check the URL and your internet connection. The website might be blocking automated requests.")