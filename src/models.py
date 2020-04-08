from typing import List
from src import utils

from cached_property import cached_property
import pandas as pd


class TextMessage:

    def __init__(self, content: str = ""):
        self.content = content.encode("ascii", "ignore").decode("utf-8")

    def __str__(self):
        return self.content


class Sticker:

    def __init__(self, uri: str, *args, **kwargs):
        self.content = uri

    def __str__(self):
        return self.content


class _Photo:

    def __init__(self, uri: str, *args, **kwargs):
        self.content = uri

    def __str__(self):
        return self.content


class Photos:

    def __init__(self, photos: List[_Photo]):
        self.content = [p.content for p in photos]


class Message:

    def __init__(self, sender_name: str, timestamp_ms: int, content: str = "", photos=None, sticker=None, *args, **kwargs):
        self.printable_sender_name = sender_name
        self.sender_name = sender_name.lower().replace(" ", "")
        self.timestamp_ms = timestamp_ms
        self.timestamp_utc = utils.timestamp_ms_to_utc_date(timestamp_ms)
        if content:
            self._text = TextMessage(content=content)
        if sticker:
            self._sticker = Sticker(**sticker)
        if photos:
            self._photos = [_Photo(**photo) for photo in photos]

    @property
    def content(self):
        if hasattr(self, '_text'):
            return self._text.content
        if hasattr(self, '_sticker'):
            return self._sticker
        if hasattr(self, '_photos'):
            return self._photos
        return

    def __str__(self):
        return str(self.sender_name + ":::" + str(self.content))


class Friend:

    def __init__(self, name: str, timestamp: int, printable_name: str = "", messages: List[Message] = None, *args, **kwargs):
        self.printable_name: str = printable_name
        self.name: str = name
        self.friend_since: int = timestamp
        if not messages:
            messages = []
        self.messages: List[Message] = messages

    @cached_property
    def messages_dataframe(self):
        msg_dict = {
            "friend": [],
            "content": [],
            "action": [],
            "timestamp": [],
        }
        for m in self.messages:
            msg_dict["friend"].append(self.name)
            msg_dict["content"].append(m.content)
            if m.sender_name == self.name:
                msg_dict["action"].append("received")
            else:
                msg_dict["action"].append("sent")
            msg_dict["timestamp"].append(m.timestamp_ms)
        return pd.DataFrame(msg_dict)


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
            if msg.sender_name == self.friend.name:
                if isinstance(msg.content, TextMessage):
                    self.__received_msg_cnt += 1
                    self.__received_char_cnt += len(str(msg.content))
            elif self.sender_name:
                if isinstance(msg.content, TextMessage):
                    self.__sent_msg_cnt += 1
                    self.__sent_char_cnt += len(str(msg.content))

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

    @cached_property
    def get_combined_messages_dataframe(self):
        msg_dfs = [f.messages_dataframe for f in self.friends()]
        return pd.concat(msg_dfs)
