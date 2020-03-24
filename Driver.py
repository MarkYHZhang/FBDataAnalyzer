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


if __name__ == '__main__':
    fb_analyzer = FBAnalyzer(root_path=get_root_path_from_input())
    top_10_friends_tuple = fb_analyzer.sorted_descending_msg_count()[:10]
    import pprint
    from collections import OrderedDict
    pp = pprint.PrettyPrinter(indent=4)
    for friend_name, msg_cnt_total in top_10_friends_tuple:
        friend_metric = FriendMetric(fb_analyzer.fb_data.sender_name, fb_analyzer.fb_data.friends.get(friend_name))
        print("-" * 80)
        info = OrderedDict({
            "name": friend_name,
            "sent_messages": friend_metric.sent_messages_count,
            "received_messages": friend_metric.received_messages_count,
            "sent_chars": friend_metric.sent_characters_count,
            "received_chars": friend_metric.received_messages_count,
            "received_per_sent_msg_ratio": friend_metric.received_messages_count/friend_metric.sent_messages_count,
            "received_per_sent_char_ratio": friend_metric.received_characters_count/friend_metric.sent_characters_count
        })
        pp.pprint(info)
        print("-" * 80)
    import ipdb; ipdb.set_trace()