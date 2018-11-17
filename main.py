from discord_hooks import Webhook
from globalv import data_json
from weibo_api.weibo_api.client import WeiboClient
import time
import html2text
h = html2text.HTML2Text()
h.ignore_links = True


client = WeiboClient()
p = client.people('5732523783')
url = data_json["Discord"]["WEBHOOK_URL"]
hook = Webhook(url, content="test3",
               username=str(p.name),
               avatar=p.avatar)


def convert_content(htmlcontent):
    markdown_content = h.handle(htmlcontent)

    try:
        content, _ = markdown_content.split("\n活动详情请阅")
    except ValueError:
        content = markdown_content
    return content


data_json["Weibo"]["LAST_WEIBO_ID"] = ""
count = 0
while True:

    """fetch without username/passwords"""
    for status in p.statuses.page(1):
        if status.isTop is None:
            if status.id != data_json["Weibo"]["LAST_WEIBO_ID"]:
                hook.set_content(convert_content(status.longTextContent))
                if status.original_pic is not None:
                    hook.set_image(status.original_pic)
                hook.set_footer(text=u"发布时间：{}".format(status.created_at))
                data_json["Weibo"]["LAST_WEIBO_ID"] = status.id
                # hook.post()
            break
    count = count + 1
    print(count)d
    time.sleep(200)



# from my_weibo_api.weiboclient import Client
# c = Client()
# c.revoke_token()
# c.get_token()
# c.set_client()
#
# while True:
#     # print("token expires in: " + str(c.token_expire_date()) + " sec")
#     # todo: renew token if it is about to expire
#
#     # check fetching limits
#     lim = c.get_weibo_package("account/rate_limit_status")
#     print("remaining ip hits: " + str(lim["remaining_ip_hits"]))
#
#     if lim["remaining_ip_hits"] <= 1:
#         print("continue after " + str(lim["reset_time_in_seconds"]) + " seconds")
#         time.sleep(lim["reset_time_in_seconds"])
#         break
#
#     result = c.get_weibo_package("statuses/home_timeline")  # fetch posts
#     b = WorthPosting(result["statuses"][0])  # check worthy to post
#     if b.worthy() is True:
#         embed = Weibo2DiscordWebhook(result["statuses"][0])  # convert to discord file
#         embed.post()  # post to discord
#
#     time.sleep(200)  # limit rate of fetching from weibo = 150/hr, min=24? sec/ping
#
