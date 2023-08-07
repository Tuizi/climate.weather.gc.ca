# Download Data Script

## Description

This script is used to download data for specified stations and years.

## Requirements

- Python 3.x

## Installation

Install the required packages using the following command:

```sh
pip install -r requirements.txt
```

## How to Run

You can run this script using the following command:

```sh
python download_data.py [--province PROVINCE] [--station_id STATION_ID] [--year YEAR]
```

### Arguments

- `--province`: Specify the province.
- `--station_id`: Specify the station ID (integer).
- `--year`: Specify the year (integer). Default is 2015.

## Notes

Make sure to configure the script with the proper URLs or file paths before running.
