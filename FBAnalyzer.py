from collections import Counter

from FBDeserializer import FBDeserializer
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

    def get_msg_freq_minutes_since_midnight(self, msg_sent=True):
        counter = Counter()
        for friend in self.fb_data.friends.friends():
            messages = friend.messages
            for m in messages:
                if msg_sent and m.sender_name == self.fb_data.sender_name or not msg_sent and m.sender_name != self.fb_data.sender_name:
                    d = m.timestamp_utc
                    from dateutil import tz
                    from_zone = tz.gettz('UTC')
                    to_zone = tz.gettz('America/New_York')
                    utc = d.replace(tzinfo=from_zone)
                    easternTime = utc.astimezone(to_zone)
                    from datetime import datetime, timedelta
                    if datetime(year=2019, month=5, day=2, tzinfo=tz.UTC) <= easternTime <= datetime(year=2019, month=8, day=25, tzinfo=tz.UTC):
                        easternTime -= timedelta(hours=3)
                    minutes_since_midnight = round((easternTime - easternTime.replace(hour=0, minute=0, second=0,
                                                                                      microsecond=0)).total_seconds()/60/15)
                    counter[minutes_since_midnight] += 1
        return sorted(counter.items())
