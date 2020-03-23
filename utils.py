import os
import logging
import json


def is_ascii(s: str):
    return all(ord(c) < 128 for c in s)


def is_valid_path(path: str):
    return os.path.isdir(path) or os.path.isfile(path)


def is_nonempty_dir(path: str):
    if not is_valid_path(path) or not os.listdir(path):
        return False
    return True


def get_path_from_input(prompt: str):
    path = None
    first = True
    while not path or not is_valid_path(path):
        if not first:
            logging.warning("Path '" + path + "' is not valid! Please re-enter...")
        else:
            first = False
        path = input(prompt)
    return path


def read_json(path):
    if not is_valid_path(path):
        return None
    with open(path) as f:
        return json.load(f)
