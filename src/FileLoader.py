import csv
import os

from src.Parsers import Parser


def load_csv(file_name, parser: Parser):
    results = []
    with open(file_name, newline='', encoding='UTF8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)
        for index, row in enumerate(reader):
            results.append(parser.parse(row))
    return results


def list_csv(file_path):
    return [f for f in os.listdir(file_path) if f.endswith('csv')]
