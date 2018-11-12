from weiboclient import Client
from weibo2discordwebhook import Weibo2DiscordWebhook
from worth_posting import WorthPosting
import time


c = Client()
# c.revoke_token()
tokenInfo = c.get_new_token()
print("New access token: " + tokenInfo["access_token"])
print("New access token expires in: " + str(tokenInfo["expires_in"]) + " sec.")
c.set_client()

while True:
    print("token expires in: " + str(c.token_expire_date()) + " sec")
    # todo: renew token if it is about to expire

    result = c.get_weibo_package("statuses/home_timeline")  # fetch posts
    b = WorthPosting(result["statuses"][0])  # check worthy to post
    if b.worthy() is True:
        embed = Weibo2DiscordWebhook(result["statuses"][0])  # convert to discord file
        embed.post()  # post to discord

    time.sleep(200)  # limit rate of fetching from weibo = 150/hr, min=24? sec/ping


