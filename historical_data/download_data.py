import pandas as pd
import requests
from datetime import datetime, timedelta
import time
import os
from concurrent.futures import ThreadPoolExecutor
import sys
import argparse


def download_data(station_id, year):
    global failed_downloads
    file_name = f"data/{station_id}/{year}.csv"

    # Only re-download the current year, skip others if they exist
    if os.path.exists(file_name) and year != current_year:
        print(f"Skipped: {station_id}-{year} (already downloaded)")
        return

    url = url_pattern.format(station_id=station_id, year=year)

    try:
        # Download the CSV data with a 2-second timeout
        response = requests.get(url, timeout=2)
        response.raise_for_status()

        # Save the file with the specified naming convention
        os.makedirs(f"data/{station_id}", exist_ok=True)
        with open(file_name, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.RequestException as e:
        print(
            f"Failed: {station_id}-{year} (Status Code: {response.status_code}, Response: {response.text})")
        failed_downloads += 1
        if failed_downloads >= 5:
            print("Error: 5 downloads failed. Exiting.")
            sys.exit(1)


# Argument parser for command-line options
parser = argparse.ArgumentParser(description="Download weather data.")
parser.add_argument("--province", help="Specify the province.")
parser.add_argument("--station_id", type=int, help="Specify the station ID.")
parser.add_argument("--year", type=int, default=2015,
                    help="Specify the initial year (default is 2015).")
args = parser.parse_args()

# Read the file
file_path = './data/stations.csv'
stations_df = pd.read_csv(file_path, skiprows=3)

# Filter by province or station ID if provided
if args.province:
    stations_df = stations_df[stations_df['Province'] == args.province.upper()]
elif args.station_id:
    stations_df = stations_df[stations_df['Station ID'] == args.station_id]

# Define the URL pattern
url_pattern = "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={station_id}&Year={year}&time=&timeframe=2&submit=Download+Data"

# Get the current year
current_year = datetime.now().year

# Initialize time tracking
start_time = time.time()

# Calculate total iterations for progress
total_iterations = len(stations_df['Station ID']) * \
    (current_year - args.year + 1)
current_iteration = 0
failed_downloads = 0

# Loop through station IDs
for station_id in stations_df['Station ID']:
    # Create a thread pool for parallel downloads
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Loop through years
        for year in range(args.year, current_year + 1):
            # Pause to limit to 10 requests per second
            time.sleep(0.1)

            # Submit download task to thread pool
            executor.submit(download_data, station_id, year)

            # Update and print progress
            current_iteration += 1
            elapsed_time = time.time() - start_time
            estimated_time_remaining = (
                total_iterations - current_iteration) * (elapsed_time / current_iteration)
            eta = str(timedelta(seconds=estimated_time_remaining))
            progress = (current_iteration / total_iterations) * 100
            print(f"Progress: {progress:.2f}% - ETA: {eta}")

# Calculate total time for progress
elapsed_time = time.time() - start_time
print(f"Download completed in {str(timedelta(seconds=elapsed_time))}")
