#!/bin/bash

# URL of the CSV file to download
URL="https://collaboration.cmc.ec.gc.ca/cmc/climate/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv"

# Output file name
OUTPUT_FILE="data/stations.csv"

# Download the CSV file using curl
curl -o "$OUTPUT_FILE" "$URL"

# Check if the download was successful
if [ $? -eq 0 ]; then
  echo "Download successful! The CSV file has been saved as $OUTPUT_FILE."
else
  echo "Download failed. Please check the URL and try again."
fi
