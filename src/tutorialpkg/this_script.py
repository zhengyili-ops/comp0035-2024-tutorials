from pathlib import Path

# This script is located in the project root, so find the path to the current file and then go to the parent of that file
project_root = Path(__file__).parent

# Find the .csv file relative to the project root and join to that path the data folder and then the example.csv file
csv_file = project_root.joinpath('data', 'example.csv')
# csv_file = project_root / 'data' / 'example.csv' # this notation would also work, even though you think the '/' is only unix/macOS

# Check if the file exists, this will print 'true' if it exists
if csv_file.exists():
    print(f"CSV file found: {csv_file}")
else:
    print("CSV file not found.")