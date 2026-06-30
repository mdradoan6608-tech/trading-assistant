import json
import os


def load(path, default=None):
    if default is None:
        default = {}

    if not os.path.exists(path):
        return default

    with open(path, "r") as file:
        return json.load(file)


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as file:
        json.dump(data, file, indent=4)
