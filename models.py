import utils
from typing import Dict
import datetime


class Sticker:

    def __init__(self, uri: str, *args, **kwargs):
        self.uri = uri


class Photo:

    def __init__(self, uri: str, *args, **kwargs):
        self.uri = uri


class Message:

    def __init__(self, sender_name: str, timestamp_ms: int, content=None, photos=None, sticker=None, *args, **kwargs):
        self.sender_name = sender_name
        self.timestamp_utc = datetime.datetime.utcfromtimestamp(timestamp_ms//1000).replace(microsecond=timestamp_ms%1000*1000)
        self.content = content
        if sticker:
            self.sticker = Sticker(**sticker)
        if photos:
            self.photos = [Photo(**photo) for photo in photos]


class Friend:

    def __init__(self, name: str, timestamp: int, *args, **kwargs):
        self.printable_name = name
        self.name = name.replace(" ", "").lower()
        self.friend_since = timestamp
        self.messages = []


class FriendList:

    def __init__(self, friends_json: Dict):
        self._friend_dict = {}
        for json_obj in friends_json["friends"]:
            friend = Friend(**json_obj)
            if not utils.is_ascii(friend.name):
                continue
            self._friend_dict[friend.name] = friend

    def contains(self, name):
        return name in self._friend_dict

    def get(self, name):
        return self._friend_dict.get(name)

    def names(self):
        return list(self._friend_dict.keys())

    def friends(self):
        return list(self._friend_dict.values())
