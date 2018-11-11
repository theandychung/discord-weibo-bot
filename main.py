from weiboclient import Client
from weibo2discordwebhook import Weibo2DiscordWebhook
from worth_posting import WorthPosting
import time


c = Client()
c.get_new_token()
print("token expires in: " + str(c.token_expire_date()) + " sec")
c.set_client()

while True:
    result = c.get_weibo_package("statuses/home_timeline")  # fetch posts
    b = WorthPosting(result["statuses"][0])  # check worthy to post
    if b.worthy() is True:
        embed = Weibo2DiscordWebhook(result["statuses"][0])  # convert to discord file
        embed.post()  # post to discord

    time.sleep(30)  # limit rate of fetching from weibo = 150/hr, min=24sec/ping
    # todo: renew token if it is about to expire
    print("token expires in: " + str(c.token_expire_date()) + " sec")
