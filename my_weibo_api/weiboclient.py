from weibopy import WeiboOauth2, WeiboClient
from my_weibo_api.WeiboAPI import SinaAPI
from globalv import data_json


class Client:
    def __init__(self):
        self.client = None
        self.access_token = data_json["Weibo"]["ACCESS_TOKEN"]
        self.oauth = None

    def get_token(self, new=False):
        """
        obtain new access token or renew token if new is True
        Otherwise simply return the access token

        :param new:
        {
            True: to get new token or renew token
            False: to read the current access token
        }
        :return: access token (str)
        """
        if data_json["Weibo"]["ACCESS_TOKEN"] is "" or new is True:
            """acquire new token or renew token"""
            """step 1: Get code"""
            self.oauth = WeiboOauth2(data_json["Weibo"]["APP_KEY"],
                                data_json["Weibo"]["APP_SECRET"],
                                data_json["Weibo"]["REDIRECT_URL"])
            authorize_url = self.oauth.authorize_url
            # print(authorize_url)
            # import webbrowser
            # webbrowser.open_new(authorize_url)
            API = SinaAPI(authorize_url,
                          data_json["Weibo"]["APP_KEY"],
                          data_json["Weibo"]["REDIRECT_URL"],
                          data_json["Weibo"]["USERNAME"],
                          data_json["Weibo"]["PASSWORDS"])
            code = API.get_code_Security()  # get code from callback url
            """step 2: use code to get access token"""
            tokenInfo = self.oauth.auth_access(code)  # get access token
            data_json["Weibo"]["ACCESS_TOKEN"] = tokenInfo["access_token"] # save token
            # data_json["Weibo"]["EXPIRES_IN"] = tokenInfo["expires_in"] # save token expired in
            # self.expires_in = tokenInfo["expires_in"]
            if "ISLOCAL" in data_json:
                """save to data.json if this is running locally"""
                from dataIO import fileIO
                fileIO("data.json", "save", data_json)
        else:
            return data_json["Weibo"]["ACCESS_TOKEN"]

    def revoke_token(self):
        """delete access token in weibo server (never works)"""
        if self._token_not_empty() and self.oauth is not None:
            self.oauth.revoke_auth_access(self.access_token)
            self.access_token = ""

    def set_client(self):
        if self._token_not_empty():
            self.client = WeiboClient(data_json["Weibo"]["ACCESS_TOKEN"])
        else:
            raise ValueError("access token cannot be empty")

    def get_weibo_package(self, api):
        """
        input weibo api commands.
        api commands can be obtained from:
        http://open.weibo.com/wiki/API%E6%96%87%E6%A1%A3/en#Timeline_API

        example:
            result = a.get_weibo_package("statuses/home_timeline")
        :param api: api
        :return:
        """
        result = None
        if self.client is not None:
            result = self.client.get(suffix=api + ".json")
        return result

    def token_expire_date(self):
        if self._token_not_empty():
            t = self.oauth.get_token_info(data_json["Weibo"]["ACCESS_TOKEN"])
            return t["expire_in"]

    def _token_not_empty(self):
        """make sure token is not empty"""
        if data_json["Weibo"]["ACCESS_TOKEN"] != "":
            return True
        else:
            ValueError("ACCESS_TOKEN IS EMPTY")
            return False


if __name__ == "__main__":
    a = Client()
    a.get_token()
    a.set_client()
    a.token_expire_date()
    # result = a.get_weibo_package("statuses/home_timeline")
    result = a.get_weibo_package("account/rate_limit_status")
    print(result)