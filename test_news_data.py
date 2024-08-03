import json
import os
import sys


def test_data(data_path):
    """
    This function tests the validity and structure of the JSON data file.

    Args:
        data_path (str): Path to the JSON data file.
    """
    try:
        with open(data_path, 'rb') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {data_path}", file=sys.stderr)
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON data in file: {data_path}", file=sys.stderr)
        exit(1)

    # Basic data structure tests (modify as needed)
    if not isinstance(data, list):
        print("Error: Top level data should be a list", file=sys.stderr)
        exit(1)
    for item in data:
        if not isinstance(item, dict):
            print(f"Error: Item in data is not a dictionary: {item}", file=sys.stderr)
            exit(1)
        required_keys = ["title", "country", "date", "impact", "forecast", "previous"]
        missing_keys = [key for key in required_keys if key not in item.keys()]
        if missing_keys:
            print(f"Error: Missing required keys in data item: {missing_keys}", file=sys.stderr)
            exit(1)


def main():
    data_path = os.getenv("DATA_PATH", "ecs/news.json")
    test_data(data_path)
    print("Data seems valid!")


if __name__ == "__main__":
    main()
