"""
files.py
"""

import json
import os
import shutil


def create_or_delete(path: str):
    """
    parameters
        string

    Given a path string, either creates it if needed or removes
    all files from under it.
    """

    if not os.path.exists(path):
        os.mkdir(path)
    else:
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))


def dump_json_data(name: str, path: str, data: dict, indent: int = 4):
    """
    parameters
        string
        string
        json
        int
    """

    if not os.path.exists(path):
        raise ValueError(f"Could not find path {path}.")

    with open(os.path.join(path, f"{name}.json"), "w") as outfile:
        json.dump(data, outfile, indent=indent)


def move_files(from_path: str, to_path: str, file_type: str | None = None):
    """
    parameters
        string
        string
        (optional)
            string
    """

    if not os.path.exists(from_path):
        raise ValueError(f"Could not locate from path, {from_path}.")

    for file in os.listdir(from_path):
        if file_type == None or file.endswith(file_type):
            if not os.path.exists(to_path):
                os.mkdir(to_path)
            shutil.move(
                os.path.join(from_path, file),
                os.path.join(to_path, file),
            )
