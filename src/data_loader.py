import csv


def load_items(file_path):
    """
    Load items data from a CSV file.

    Args:
    file_path (str): The path to the CSV file containing item data.

    Returns:
    list: A list of items, where each item is represented as a tuple (width, height).
    """
    items = []
    with open(file_path, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            width = int(row["Width"])
            height = int(row["Height"])
            item = (width, height)
            items.append(item)
    return items
