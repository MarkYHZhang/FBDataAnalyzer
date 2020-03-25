from FBAnalyzer import FBAnalyzer
from models import FriendMetric

import utils
import logging
import paths


def get_root_path_from_input():
    while True:
        path = utils.get_path_from_input("Input path to FB data folder: ")
        requirements = [
            utils.is_valid_path(paths.get_friends_json_path(path)),
            utils.is_nonempty_dir(paths.get_message_inbox_path(path))
        ]
        if all(requirements):
            return path
        else:
            logging.warning(
                "Provided path '" + path + "' does not contain "
                                           "required 'friends/friends.json' and/or a nonempty messages/inbox"
            )


