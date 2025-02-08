import json
import os
from helper import archive_json

def add_to_archive(message):
    try:
        with open(archive_json, "r") as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("JSON file does not contain a list.")
    except(FileNotFoundError, json.JSONDecodeError, ValueError):
        data = []

    data.append(message)

    with open(archive_json, "w") as file:
        json.dump(data, file, indent=4)
