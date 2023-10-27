import pandas as pd


def load_sheets_from_csv(file_path):
    """
    Load sheet data from a CSV file.

    Parameters:
    - file_path (str): Path to the CSV file containing sheet data.

    Returns:
    - List[dict]: A list of dictionaries, where each dictionary represents a sheet in stock.
      Each dictionary contains the following keys:
      - 'size': Tuple representing the dimensions (width, height) of the sheet.
      - 'quantity': Integer, the available quantity of the sheet.
      - 'cost': Float, the cost of the sheet.
    - None: If there is an error during data loading, returns None.
    """
    sheets = []
    try:
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            id = int(row["Id"])
            size = (row["Width"], row["Height"])
            sheets.append({"id": id, "size": size})
        return sheets
    except Exception as e:
        print(f"Error loading stock data from {file_path}: {str(e)}")
        return None


def load_items_from_csv(file_path):
    """
    Load item data from a CSV file.

    Parameters:
    - file_path (str): Path to the CSV file containing item data.

    Returns:
    - List[dict]: A list of dictionaries, where each dictionary represents a customer demand item.
      Each dictionary contains the following keys:
      - 'size': Tuple representing the dimensions (width, height) of the item.
      - 'quantity': Integer, the required quantity of the item.
    - None: If there is an error during data loading, returns None.
    """
    items = []
    try:
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            id = int(row["Id"])
            size = (row["Width"], row["Height"])
            items.append({"id": id, "size": size})
        return items
    except Exception as e:
        print(f"Error loading demand data from {file_path}: {str(e)}")
        return None
