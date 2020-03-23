from FBDeserializer import FBDeserializer


class FBAnalyzer:

    def __init__(self, fb_data: FBDeserializer = None, root_path: str = None):
        if fb_data:
            self.fb_data = fb_data
        elif root_path:
            self.fb_data = FBDeserializer(root_path)
        else:
            raise Exception("Must provide either 'fb_data' a FBDeserializer object or 'root_path' str!")

    def sorted_descending_msg_count(self):
        sorted_list = [(friend.name, len(friend.messages)) for friend in self.fb_data.friend_list.friends()]
        return sorted(sorted_list, key=lambda x: (-x[1], x[0]))

