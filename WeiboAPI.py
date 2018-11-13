# !/usr/bin/python
# -*- coding: utf-8 -*-
import re
import json

import certifi
import urllib.request
import urllib.error
import urllib.parse
import urllib3
import http.cookiejar
import base64
# encrypt
import rsa
import binascii
"""
Note: This file originated by huan zhan
for getting code from weibo without web,
but it has been Modified by Andy Chung

# more about get code without web:
# https://blog.csdn.net/zhanh1218/article/details/26383469#commentBox
"""
"""
[Filename]
WeiboAPI.py
@author: U{The_Third_Wave/huan zhan<mailto: zhanh121823 at sina.com>}
@copyright: U{Copyright (c) 2014.05.22, huan zhan}
@contact: zhanh121823 at sina.com/QQ:563134080
@version: $1.0$
# 微博API接口
"""


class SmartRedirectHandler(urllib.request.HTTPRedirectHandler):
    """
    # 參考：風行影者/Blog：http://www.cnblogs.com/wly923/archive/2013/04/28/3048700.html
    """

    def http_error_301(cls, req, fp, code, msg, headers):
        result = urllib.request.HTTPRedirectHandler.http_error_301(cls, req, fp, code, msg, headers)
        result.status = code
        return result

    def http_error_302(cls, req, fp, code, msg, headers):
        result = urllib.request.HTTPRedirectHandler.http_error_302(cls, req, fp, code, msg, headers)
        result.status = code
        return result


def get_cookie():
    cookies = http.cookiejar.CookieJar()
    return urllib.request.HTTPCookieProcessor(cookies)


def get_opener(proxy=False):
    rv = urllib.request.build_opener(get_cookie(), SmartRedirectHandler())
    rv.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')]
    return rv


class SinaAPI():
    """
    # @author: U{The_Third_Wave/huan zhan<mailto: zhanh121823 at sina.com>}
    # get_code_NS()方法為風行影者所寫。/Blog：http://www.cnblogs.com/wly923/archive/2013/04/28/3048700.html
    # get_code_NS()明文傳輸密碼，不安全。所以作者@The_Third_Wave 用模擬登陸的方法獲取重要參數'ticket'。保證傳輸過程中不明文傳輸密碼。保證安全。
    # get_code_Security()方法為作者@The_Third_Wave所寫安全自動獲取code的方法。
    # 有疑問的請Blog：http://blog.csdn.net/zhanh1218/article/details/26383469留言或者sina微博關注作者@The_Third_Wave。
    """

    def __init__(self, CALLBACK_URL, APP_KEY, REDIRECT_URL, USER_ID, USER_PSWD):
        self.CALLBACK_URL = CALLBACK_URL
        self.APP_KEY = APP_KEY
        self.REDIRECT_URL = REDIRECT_URL
        self.USER_ID = USER_ID
        self.USER_PSWD = USER_PSWD
        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                        ca_certs=certifi.where())

    def get_username(self, USER_ID):
        # The Encryption Algorithm of username
        # ssologin.js : ah.su=sinaSSOEncoder.base64.encode(m(aj));
        USER_ID_ = urllib.parse.quote(USER_ID)  # encode username, avoid error example:@ &

        su = base64.b64encode(bytes(USER_ID_, "utf-8")).decode("utf-8")[:-1]
        return su

    def get_password_rsa(self, USER_PSWD, PUBKEY, servertime, nonce):
        # 密碼加密運算sina我已知有兩種，這是其中一種。
        # rsa Encrypt :  #when pwencode = "rsa2"
        rsaPubkey = int(PUBKEY, 16)  # pubkey from 16 to 10
        key_1 = int('10001', 16)  # 10001 to 65537
        key = rsa.PublicKey(rsaPubkey, key_1)  #
        message = str(servertime) + "\t" + str(nonce) + "\n" + str(USER_PSWD)
        passwd = rsa.encrypt(bytes(message, "utf-8"), key)
        passwd = binascii.b2a_hex(passwd)  # to 16
        return passwd

    def get_parameter(self):
        su = self.get_username(self.USER_ID)
        # su = get_username(USER_ID)‎‎
        url = "https://login.sina.com.cn/sso/prelogin.php?entry=openapi&callback=sinaSSOController.preloginCallBack\
&su=" + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.15)"
        r = self.http.request('GET', url)
        p = re.compile('\((.*)\)')
        json_data = p.search(r.data.decode('utf-8')).group(1)
        data = json.loads(json_data)

        PUBKEY = data['pubkey']
        pcid = data['pcid']
        servertime = str(data['servertime'])
        nonce = data['nonce']
        rsakv = str(data['rsakv'])
        sp = self.get_password_rsa(self.USER_PSWD, PUBKEY, servertime, nonce)

        # print pcid; print servertime; print nonce; print rsakv; print sp; print su
        return pcid, servertime, nonce, rsakv, sp, su

    def get_ticket(self):
        pcid, servertime, nonce, rsakv, sp, su = self.get_parameter()
        fields = urllib.parse.urlencode({
            'entry': 'openapi',
            'gateway': '1',
            'from': '',
            'savestate': '0',
            'useticket': '1',
            'pagerefer': '',
            'pcid': pcid,
            'ct': '1800',
            's': '1',
            'vsnf': '1',
            'vsnval': '',
            'door': '',
            'appkey': 'kxR5R',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': sp,
            'sr': '1680*1050',
            'encoding': 'UTF-8',
            'cdult': '2',
            'domain': 'weibo.com',
            'prelt': '0',
            'returntype': 'TEXT',
        })
        headers = {
            # "請求": "POST /sso/login.php?client=ssologin.js(v1.4.15)&_=1400652171542 HTTP/1.1",
            # "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            # "Referer": self.CALLBACK_URL,
            # "Accept-Language": "zh-CN",
            # "Origin": "https://api.weibo.com",
            # "Accept-Encoding": "gzip, deflate",
            # "User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ZHCNMSE; rv:11.0) like Gecko",
            # "Host": "login.sina.com.cn",
            # "Connection": "Keep-Alive",
            # "Cache-Control": "no-cache",
        }
        url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)"
        req = urllib.request.Request(url, fields, headers)
        req.data = bytes(req.data, "utf-8")
        f = urllib.request.urlopen(req)
        data = json.loads(f.read())
        return data["ticket"]

    def get_code_Security(self):
        ticket = self.get_ticket()
        fields = urllib.parse.urlencode({
            'action': 'submit',  # 必須
            'display': 'default',
            'withOfficalFlag': '0',  # 必須
            'quick_auth': 'null',
            'withOfficalAccount': '',
            'scope': '',
            'ticket': ticket,  # 必須
            'isLoginSina': '',
            'response_type': 'code',  # 必須
            'regCallback': 'https://api.weibo.com/2/oauth2/authorize?client_id=' + self.APP_KEY + '\
&response_type=code&display=default&redirect_uri=' + self.REDIRECT_URL + '&from=&with_cookie=',
            'redirect_uri': self.REDIRECT_URL,  # 必須
            'client_id': self.APP_KEY,  # 必須
            'appkey62': 'kxR5R',
            'state': '',  # 必須
            'verifyToken': 'null',
            'from': '',  # 必須
            'userId': "",  # 此方法不需要填寫明文ID
            'passwd': "",  # 此方法不需要填寫明文密碼
        })
        LOGIN_URL = 'https://api.weibo.com/oauth2/authorize'
        headers = {"User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ZHCNMSE; rv:11.0) like Gecko",
                   "Referer": self.CALLBACK_URL,
                   "Content-Type": "application/x-www-form-urlencoded",
                   }
        req = urllib.request.Request(LOGIN_URL, fields, headers)
        req.data = bytes(req.data, "utf-8")
        req_ = urllib.request.urlopen(req)
        return_redirect_uri = req_.geturl()
        code = ''.join(re.findall(r"(?<=code%3D).{32}|(?<=code=).{32}", return_redirect_uri))  # url中=用%3D表示或者=直接表示
        return code


if __name__ == "__main__":
    from globalv import data_json

    APP_KEY = data_json["APP_KEY"]
    APP_SECRET = data_json["APP_SECRET"]
    REDIRECT_URL = data_json["REDIRECT_URL"]
    USERNAME = data_json["USERNAME"]
    PASSWORDS = data_json["PASSWORDS"]

    from weibopy import WeiboOauth2
    client = WeiboOauth2(APP_KEY, APP_SECRET, REDIRECT_URL)
    authorize_url = client.authorize_url

    API = SinaAPI(authorize_url, APP_KEY, REDIRECT_URL, USERNAME, PASSWORDS)
    code = API.get_code_Security()  # get code from callback url
    auth = client.auth_access(code)  # get access token
    # print(auth["access_token"])
    from weibopy import WeiboClient
    client = WeiboClient(auth["access_token"])
    result = client.get(suffix="statuses/home_timeline.json")
    for st in result["statuses"]:
        print(st['text'])