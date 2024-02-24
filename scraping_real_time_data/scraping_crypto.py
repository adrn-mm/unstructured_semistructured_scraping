from pycoingecko import CoinGeckoAPI
import pandas as pd
import subprocess
from datetime import datetime
import os

# Initialize CoinGeckoAPI
cg = CoinGeckoAPI()

# Parameters for the API call
parameters = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 100,
    'page': 1,
    'sparkline': False,
    'locale': 'en'
}

# Fetch coin market data
coin_market_data = cg.get_coins_markets(**parameters)

# Convert to DataFrame and drop unnecessary columns
df = pd.DataFrame(coin_market_data)
df = df.drop([
    'id', 'symbol', 'image', 'high_24h', 'low_24h', 'price_change_24h', 'price_change_percentage_24h',
    'market_cap_change_24h', 'market_cap_change_percentage_24h', 'fully_diluted_valuation', 'ath_date', 
    'ath_change_percentage', 'atl_change_percentage', 'atl_date', 'roi', 'market_cap', 'circulating_supply', 
    'total_supply', 'max_supply', 'ath', 'atl', 'market_cap_rank', 'total_volume'
], axis=1)

# Generate a timestamped file name for the CSV
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
csv_file_name = f"coin_market_data_{timestamp}.csv"
csv_file_path = os.path.join('/tmp', csv_file_name)

# Save DataFrame to CSV
df.to_csv(csv_file_path, index=False)

# Define the HDFS destination directory
hdfs_dir = '/user/csso_adrian.muhammad/scraping'
hdfs_file_path = os.path.join(hdfs_dir, csv_file_name)

# Create the directory in HDFS (ignore if exists)
subprocess.call(['hadoop', 'fs', '-mkdir', '-p', hdfs_dir])
# Upload the CSV to HDFS (overwrite if exists)
subprocess.call(['hadoop', 'fs', '-put', '-f', csv_file_path, hdfs_file_path])

# Hive external table creation/update command to reflect new CSV file
hive_query = f"""
    DROP TABLE IF EXISTS scraping_crypto;
    CREATE EXTERNAL TABLE scraping_crypto (
        name STRING,
        current_price FLOAT,
        last_updated STRING
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    STORED AS TEXTFILE
    LOCATION '{hdfs_dir}';
    """

hive_cmd = ['hive', '-e', hive_query]
subprocess.run(hive_cmd, check=True)

# Clean up the local temporary file
os.remove(csv_file_path)

print("Data ingestion to HDFS and Hive external table update/creation is completed with the latest data.")