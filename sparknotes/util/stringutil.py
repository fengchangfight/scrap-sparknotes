class StringUtil:

    def __init__(self):
        pass

    # ==fc== get first in a list, if empty, return default
    @staticmethod
    def get_first(in_list, if_empty):
        if len(in_list) > 0:
            return in_list[0]
        else:
            return if_empty
