from collections import Counter

from FBDeserializer import FBDeserializer
from models import Friend
import utils

import pickle


class FBAnalyzer:

    @staticmethod
    def get_pickle_instance(path_to_pickle):
        with open(path_to_pickle, 'rb') as input:
            fb_analyzer: FBAnalyzer = pickle.load(input)
            return fb_analyzer

    def __init__(self, fb_data: FBDeserializer = None, root_path: str = None):
        if fb_data:
            self.fb_data = fb_data
        elif root_path:
            self.fb_data = FBDeserializer(root_path)
        else:
            raise Exception("Must provide either 'fb_data' a FBDeserializer object or 'root_path' str!")

    def save_to_pickle(self, path_to_pickle):
        with open(path_to_pickle, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def sorted_descending_msg_count(self):
        sorted_list = [(friend.name, len(friend.messages)) for friend in self.fb_data.friends.friends()]
        return sorted(sorted_list, key=lambda x: (-x[1], x[0]))

    def __get_msg_freq_minutes_since_midnight(self, friend: Friend, msg_sent=True):
        counter = Counter({k: 0 for k in range(1440)})
        messages = friend.messages
        for m in messages:
            if msg_sent and m.sender_name == self.fb_data.sender_name or not msg_sent and m.sender_name != self.fb_data.sender_name:
                eastern_datetime = utils.utc_to_eastern_datetime(m.timestamp_utc)
                minutes_since_midnight = round((eastern_datetime - eastern_datetime.replace(hour=0, minute=0, second=0,
                                                                                  microsecond=0)).total_seconds()/60)
                counter[minutes_since_midnight] += 1
        return counter

    def get_msg_freq_minutes_since_midnight(self, friend: Friend, msg_sent=True):
        return sorted(self.__get_msg_freq_minutes_since_midnight(friend=friend, msg_sent=msg_sent).items())

    def get_all_msg_freq_minutes_since_midnight(self, msg_sent=True):
        counter = Counter({k: 0 for k in range(1440)})
        for friend in self.fb_data.friends.friends():
            counter += self.__get_msg_freq_minutes_since_midnight(friend=friend, msg_sent=msg_sent)
        for i in range(1440):
            if i not in counter:
                counter[i] = 0
        return sorted(counter.items())
