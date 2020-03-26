import utils
from typing import Dict, List
import datetime


class Sticker:

    def __init__(self, uri: str, *args, **kwargs):
        self.uri = uri


class Photo:

    def __init__(self, uri: str, *args, **kwargs):
        self.uri = uri


class Message:

    def __init__(self, sender_name: str, timestamp_ms: int, content: str = "", photos=None, sticker=None, *args, **kwargs):
        self.printable_sender_name = sender_name
        self.sender_name = sender_name.lower().replace(" ", "")
        self.timestamp_utc = datetime.datetime.utcfromtimestamp(timestamp_ms//1000).replace(microsecond=timestamp_ms%1000*1000)
        self.content: str = content
        if sticker:
            self.sticker = Sticker(**sticker)
        if photos:
            self.photos = [Photo(**photo) for photo in photos]

    def __str__(self):
        return str(self.sender_name + ":::" + self.content)


class Friend:

    def __init__(self, name: str, timestamp: int, printable_name: str = "", messages: List[Message] = None, *args, **kwargs):
        self.printable_name: str = printable_name
        self.name: str = name
        self.friend_since: int = timestamp
        if not messages:
            messages = []
        self.messages: List[Message] = messages


class FriendMetric:

    __received_msg_cnt = 0
    __sent_msg_cnt = 0

    @property
    def received_messages_count(self):
        return self.__received_msg_cnt

    @property
    def sent_messages_count(self):
        return self.__sent_msg_cnt

    @property
    def total_messages_count(self):
        return self.__received_msg_cnt + self.__sent_msg_cnt

    __received_char_cnt = 0
    __sent_char_cnt = 0

    @property
    def received_characters_count(self):
        return self.__received_char_cnt

    @property
    def sent_characters_count(self):
        return self.__sent_char_cnt

    @property
    def total_characters_count(self):
        return self.__received_char_cnt + self.__sent_char_cnt

    def __process_msgs(self):
        for msg in self.friend.messages:
            if msg.sender_name == self.friend.id:
                self.__received_msg_cnt += 1
                self.__received_char_cnt += len(msg.content)
            elif self.sender_name:
                self.__sent_msg_cnt += 1
                self.__sent_char_cnt += len(msg.content)

    def __init__(self, sender_name: str,  friend: Friend):
        self.sender_name: str = sender_name
        self.friend: Friend = friend
        self.__process_msgs()

    def __str__(self):
        return str({
            "received_mess"
        })


class FriendList:

    def __init__(self, friends: List[Friend]):
        self._friend_dict = {}
        for f in friends:
            self._friend_dict[f.name] = f

    def contains(self, name):
        return name in self._friend_dict

    def get(self, name):
        return self._friend_dict.get(name)

    def names(self):
        return list(self._friend_dict.keys())

    def friends(self):
        return list(self._friend_dict.values())
