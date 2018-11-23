# from dataIO import fileIO
from global_values import data_json

"""
This file is to check if the weibo post is worth transferring to discord.
"""


class WorthPosting:
    def __init__(self, r):
        self.result = r
        if "LAST_WEIBO_ID" not in data_json["Weibo"]:
            data_json["Weibo"]["LAST_WEIBO_ID"] = ""

    def is_it_new_post(self, idstr):
        """
        check if the latest post is new by
        checking if its idstr is the same as
        the saved one in data.json
        :param idstr: weibo id (str)
        :return:
        {
            True: if it is (and save)
            False: not new
        }
        """
        # if idstr != self.data_json["Weibo"]["LAST_WEIBO_ID"]:
        #     self.data_json["Weibo"]["LAST_WEIBO_ID"] = idstr
        #     fileIO("data.json", "save", self.data_json)
        #     return True
        # return False
        if idstr != data_json["Weibo"]["LAST_WEIBO_ID"]:
            data_json["Weibo"]["LAST_WEIBO_ID"] = idstr
            return True
        return False

    def more(self):
        """ maybe add more in the future """
        pass

    def worthy(self):
        w = False
        if self.is_it_new_post(self.result["idstr"]) is True:
            w = True
        return w


if __name__ == "__main__":
    a = WorthPosting(r="")
    print(a.is_it_new_post("4304516176326344"))