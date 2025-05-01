# python csv_handler.py
import csv
import sys
import os

def fill_empty_cells(csv_file):
    """
    Reads a CSV file, fills empty cells with "none", and writes the changes back to the file.

    Args:
        csv_file (str): The path to the CSV file.
    """
    try:
        if not os.path.exists(csv_file):
          print(f"Error: File '{csv_file}' does not exist.")
          sys.exit(1)
        
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Get the header row
            data = list(reader)  # Read all rows into memory

        # Iterate through the data and fill empty cells
        for row in data:
            for i in range(len(row)):
                if not row[i]:  # Check for empty string
                    row[i] = "none"

        # Write back to the CSV file, using the original header
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write the header row
            writer.writerows(data)  # Write the modified data rows

        print(f"File '{csv_file}' processed successfully. Empty cells filled with 'none'.")

    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python csv_handler.py <csv_file_path>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    fill_empty_cells(csv_file_path)