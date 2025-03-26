import pandas as pd
import glob
import os
from get_details import FIELDS

def main():
    # Define the path pattern for the CSV files
    file_pattern = os.path.join("detail_groups", "details_*_*.csv")
    
    # Use glob to find all matching files
    csv_files = glob.glob(file_pattern)
    
    # Open the output file for writing
    with open("big_details.csv", "w") as outfile:
        for i, file in enumerate(csv_files):
            with open(file, "r") as infile:
                # Copy the header only from the first file
                if i == 0:
                    outfile.write(infile.read())
                else:
                    # Skip the header for subsequent files
                    next(infile)
                    outfile.write(infile.read())
    
    print(f"Combined {len(csv_files)} files into 'big_details.csv'.")

if __name__ == "__main__":
    main()