import os
import logging
import json
from src import paths
import datetime
from dateutil import tz


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


def get_root_path_from_input():
    while True:
        path = get_path_from_input("Input path to FB data folder: ")
        requirements = [
            is_valid_path(paths.get_friends_json_path(path)),
            is_nonempty_dir(paths.get_message_inbox_path(path))
        ]
        if all(requirements):
            return path
        else:
            logging.warning(
                "Provided path '" + path + "' does not contain "
                                           "required 'friends/friends.json' and/or a nonempty messages/inbox"
            )


def read_json(path):
    if not is_valid_path(path):
        return None
    with open(path) as f:
        return json.load(f)


def timestamp_ms_to_utc_date(timestamp_ms: int):
    return datetime.datetime.utcfromtimestamp(timestamp_ms//1000).replace(microsecond=timestamp_ms%1000*1000)


def utc_to_eastern_datetime(utc_datetime: datetime.datetime):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    utc = utc_datetime.replace(tzinfo=from_zone)
    eastern_datetime = utc.astimezone(to_zone)
    return eastern_datetime
