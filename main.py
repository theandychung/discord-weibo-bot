from weiboclient import Client
from weibo2discordwebhook import Weibo2DiscordWebhook
from worth_posting import WorthPosting
import time


a = Client()
# a.get_new_token()
a.set_client()

# while True:
result = a.get_weibo_package("statuses/home_timeline")  # fetch posts
b = WorthPosting(result["statuses"][0])  # check worthy to post
if b.worthy() is True:
    """
    todo: renew token if it is about to expire
    """
    embed = Weibo2DiscordWebhook(result["statuses"][0])  # convert to discord file
    embed.post()  # post to discord
# time.sleep(25)  # limit rate of fetching from weibo = 150/hr
