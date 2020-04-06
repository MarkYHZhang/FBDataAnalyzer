from src.FBAnalyzer import FBAnalyzer
from src.utils import get_root_path_from_input
from src.models import FriendMetric

if __name__ == '__main__':
    fb_analyzer = FBAnalyzer(root_path=get_root_path_from_input())
    # fb_analyzer = FBAnalyzer.get_pickle_instance("../FBAnalyzer.pkl")

    top_10_friends_tuple = fb_analyzer.sorted_descending_msg_count()[:10]
    from collections import OrderedDict
    char_ratio_list = []
    rank = 1
    for friend_name, msg_cnt_total in top_10_friends_tuple:
        friend_metric = FriendMetric(fb_analyzer.fb_data.sender_name, fb_analyzer.fb_data.friends.get(friend_name))
        info = OrderedDict({
            "name": friend_name,
            "rank": rank,
            "sent_messages": friend_metric.sent_messages_count,
            "received_messages": friend_metric.received_messages_count,
            "total_messages": friend_metric.total_messages_count,
            "sent_chars": friend_metric.sent_characters_count,
            "received_chars": friend_metric.received_characters_count,
            "total_chars": friend_metric.total_characters_count,
            "received_per_sent_msg_ratio": friend_metric.received_messages_count/max(1,friend_metric.sent_messages_count),
            "received_per_sent_char_ratio": friend_metric.received_characters_count/max(1,friend_metric.sent_characters_count),
        })
        rank += 1
        for k, v in info.items():
            print(k + ":", v)
        print("-" * 60)