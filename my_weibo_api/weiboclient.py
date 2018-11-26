from weibopy import WeiboOauth2, WeiboClient
from my_weibo_api.WeiboAPI import SinaAPI
from global_values import data_json


class Client:
    def __init__(self):
        self.client = None
        self.oauth = None
        if self._token_found() is True:
            self.access_token = data_json["Weibo"]["access_token"]
        else:
            self.access_token = ""

    def get_token(self):
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
        if self._token_found() is False:
            """acquire new token or renew token"""
            """step 1: Get code"""
            self.oauth = WeiboOauth2(data_json["Weibo"]["app_key"],
                                data_json["Weibo"]["app_secret"],
                                data_json["Weibo"]["redirect_url"])
            authorize_url = self.oauth.authorize_url
            # print(authorize_url)
            # import webbrowser
            # webbrowser.open_new(authorize_url)
            API = SinaAPI(authorize_url,
                          data_json["Weibo"]["app_key"],
                          data_json["Weibo"]["redirect_url"],
                          data_json["Weibo"]["username"],
                          data_json["Weibo"]["passwords"])
            code = API.get_code_Security()  # get code from callback url
            """step 2: use code to get access token"""
            tokenInfo = self.oauth.auth_access(code)  # get access token
            data_json["Weibo"]["access_token"] = tokenInfo["access_token"] # save token
            self.access_token = tokenInfo["access_token"]
            if "islocal" in data_json["Weibo"]:
                """save to data.json if this is running locally"""
                from dataIO import fileIO
                fileIO("data.json", "save", data_json)
        else:
            return data_json["Weibo"]["access_token"]

    def revoke_token(self):
        """delete access token in weibo server (never works)"""
        if self._token_found() and self.oauth is not None:
            self.oauth.revoke_auth_access(self.access_token)
            self.access_token = ""

    def set_client(self):
        if self._token_found():
            self.client = WeiboClient(data_json["Weibo"]["access_token"])
        else:
            raise ValueError("access token needed to set client")

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
        if self._token_found() and self.oauth is not None:
            t = self.oauth.get_token_info(data_json["Weibo"]["access_token"])
            return t["expire_in"]
        else:
            raise ValueError("token expire date called but no token found")

    def _token_found(self):
        """make sure token is not empty"""
        if "access_token" not in data_json["Weibo"] \
                or data_json["Weibo"]["access_token"] == "":
            return False
        else:
            return True


if __name__ == "__main__":
    a = Client()
    a.get_token()
    a.set_client()
    a.token_expire_date()
    # result = a.get_weibo_package("statuses/home_timeline")
    result = a.get_weibo_package("account/rate_limit_status")
    print(result)