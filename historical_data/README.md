## Explanation
The script now accepts either a province or a station ID as a command-line argument. If neither is provided, it downloads data for all stations.
The downloads are stored in the data folder, with subfolders for each station ID. The file naming format is year-month.
The script checks if a file already exists before downloading, except for the current month of the current year.
A timeout of 2 seconds is applied to each download, and the script exits with an error if 5 downloads fail.
Progress is logged as a percentage, along with an estimated time to completion (ETA).

## Usage Examples
Download data for a specific station ID: `python script_name.py 1234`
Download data for a specific province: `python script_name.py QUEBEC`
Download data for all stations: python `script_name.py`