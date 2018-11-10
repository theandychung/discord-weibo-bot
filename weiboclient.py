from dataIO import fileIO
from weibopy import WeiboOauth2, WeiboClient
from WeiboAPI import SinaAPI
from globalv import data_json


class Client:
    def __init__(self):
        self.client = None
        self.expires_in = ""
        self.access_token = ""
        self.oauth = None

    def get_new_token(self):
        """
        obtain new access token or renew token
        :return: token information package
        example:
        {
            'access_token': '2.00E9E_TFjnd8tDa4ab7f82cbja8DTE',
            'remind_in': '157679999',
            'expires_in': 157679999,
            'uid': '1231231234',
            'isRealName': 'true'
        }

        """
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
        # print(Oauth.auth_access("bf77dfb8fc0339a77ff4fe30bea24cd4"))
        tokenInfo = self.oauth.auth_access(code)  # get access token
        data_json["Weibo"]["ACCESS_TOKEN"] = tokenInfo["access_token"] # save token
        data_json["Weibo"]["EXPIRES_IN"] = tokenInfo["expires_in"] # save token expired in
        self.expires_in = tokenInfo["expires_in"]
        # fileIO("data.json", "save", data_json)
        return tokenInfo

    def set_client(self):
        if self._token_valid():
            self.client = WeiboClient(data_json["Weibo"]["ACCESS_TOKEN"])

    def get_weibo_package(self, api):
        """
        input weibo api commands
        example:
            result = a.do_something("statuses/home_timeline")
        :param api: api
        :return:
        """
        result = None
        if self.client is not None:
            result = self.client.get(suffix=api + ".json")
        return result

    def token_expire_date(self):
        if self._token_valid():
            t = self.oauth.get_token_info(data_json["Weibo"]["ACCESS_TOKEN"])
            return t["expire_in"]

    def _token_valid(self):
        if data_json["Weibo"]["ACCESS_TOKEN"] != "":
            return True
        else:
            ValueError("ACCESS_TOKEN IS EMPTY")
            return False


if __name__ == "__main__":
    a = Client()
    a.get_new_token()
    a.set_client()
    import time
    time.sleep(5)
    a.token_expire_date()
    # result = a.get_weibo_package("statuses/home_timeline")
    # print(result["statuses"][0]['text'])