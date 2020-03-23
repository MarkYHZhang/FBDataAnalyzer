import os


def get_friends_json_path(root):
    return os.path.join(root, "friends", "friends.json")


def get_message_inbox_path(root):
    return os.path.join(root, "messages", "inbox")
