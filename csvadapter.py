# Interaction with data file CSV
import csv


# File in current directory
FILE = 'data.csv'


def add_row(fields: list) -> None:
    """Add 1 row in data file. """
    assert len(fields) == 4, 'should be 4 fields'
    with open(FILE, 'a', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(fields)


def read_fieldnames():
    """Read field names in data file."""
    with open(FILE, 'r', encoding='utf-8', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        field_names = reader.fieldnames
        return field_names


def read_rows() -> list:
    """Read CSV file and return list of dict."""
    with open(FILE, 'r', encoding='utf-8') as csv_file:
        read = csv.DictReader(csv_file)
        rows = [row for row in read]
    return normalize_rows(rows)


def normalize_rows(rows: list) -> list:
    """Normalize data types for "category_id" and "cost"."""
    if rows is None:
        return None

    for row in rows:
        row['category_id'] = int(row['category_id'])
        row['cost'] = round(float(row['cost']), 2)
    return rows
