import sys

from utils.filter_csv import parse_csv


def run_processor(filepath):
    """Run the csv parse function."""
    try:
        # get the name of the file
        file_name = filepath.split("/")[-1]
        parse_csv(filepath, file_name)
        print("'Output CSV file created'")
    except FileNotFoundError:
        print("File Not Found")
    except ValueError:
        print("File not a valid CSV")
    return


if __name__ == "__main__":
    filepath = sys.argv[1]
    run_processor(filepath)
