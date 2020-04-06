import os
from collections import Counter
from typing import List

from src.models import FriendList, Message, Friend
from src import paths, utils


class FBDeserializer:

    def __read_messages(self, inbox_path):
        messages = []
        oldest_timestamp_ms = 100000000000000
        for msg_file in os.scandir(inbox_path):
            if not msg_file.is_file() or not msg_file.name.startswith("message_"):
                continue
            json = utils.read_json(msg_file.path)
            for participant in json["participants"]:
                self.__name_inference_counter[participant["name"]] += 1
            for msg_json in json["messages"]:
                messages.append(Message(**msg_json))
                oldest_timestamp_ms = min(oldest_timestamp_ms, msg_json["timestamp_ms"])
        return messages, oldest_timestamp_ms

    def __construct_friend_list(self):
        name_counter = Counter()
        inbox_messages_path = paths.get_message_inbox_path(self.root_path)
        friends: List[Friend] = []
        self.__name_inference_counter = Counter()
        for inbox in os.scandir(inbox_messages_path):
            if not inbox.is_dir():
                continue
            msg_one_json = utils.read_json(os.path.join(inbox, "message_1.json"))

            thread_type: str = msg_one_json["thread_type"]
            # only dealing with 1-on-1 messages, not groups yet.
            if thread_type != "Regular":
                continue

            printable_name: str = msg_one_json["title"].strip()

            # to deal with duplicate names (both first and last)
            formatted_name: str = printable_name.replace(" ", "").lower()
            if formatted_name in name_counter:
                formatted_name += "_" + str(name_counter[formatted_name])
            name_counter[formatted_name] += 1

            messages, oldest_message = self.__read_messages(inbox.path)

            friends.append(
                Friend(
                    name=formatted_name,
                    printable_name=printable_name,
                    timestamp=oldest_message,
                    messages=messages
                )
            )
        self.sender_name = self.__name_inference_counter.most_common(1)[0][0].lower().replace(" ", "")
        return friends

    def __init__(self, root_path):
        self.root_path = root_path
        self.friends = FriendList(self.__construct_friend_list())
