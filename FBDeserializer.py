import utils
import os
from collections import Counter

from models import FriendList, Message
import paths


class FBDeserializer:

    def __read_messages(self, inbox_path):
        messages = []
        for msg_file in os.scandir(inbox_path):
            if not msg_file.is_file() or not msg_file.name.startswith("message_"):
                continue
            json = utils.read_json(msg_file.path)
            for participant in json["participants"]:
                self.__name_inference_counter[participant["name"]] += 1
            for msg_json in json["messages"]:
                messages.append(Message(**msg_json))
        return messages

    def _populate_messages(self):
        self.__name_inference_counter = Counter()
        for msg_inbox in os.scandir(paths.get_message_inbox_path(self.root_path)):
            if not msg_inbox.is_dir():
                continue
            formatted_name = msg_inbox.name.split("_")[0].lower()
            if self.friend_list.contains(formatted_name):
                friend = self.friend_list.get(formatted_name)
                friend.messages = self.__read_messages(msg_inbox.path)
        self.user = self.friend_list.get(self.__name_inference_counter.most_common(1)[0][0].lower().replace(" ", ""))

    def __init__(self, root_path):
        self.root_path = root_path
        self.friend_list = FriendList(utils.read_json(paths.get_friends_json_path(self.root_path)))
        self._populate_messages()

