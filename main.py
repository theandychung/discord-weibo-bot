from discord_hooks import Webhook
from globalv import data_json
from weibo_api.weibo_api.client import WeiboClient
import time
import html2text
from my_weibo_api.weiboclient import Client
# from my_weibo_api.worth_posting import WorthPosting
from my_weibo_api.weibo2discordwebhook import Weibo2DiscordWebhook


# init
count = 0
sleep_time = 200


def worth(post_id): # check worthy to post
    if "LAST_WEIBO_ID" not in data_json["Weibo"]:
        data_json["Weibo"]["LAST_WEIBO_ID"] = ""
    if post_id != data_json["Weibo"]["LAST_WEIBO_ID"]:
        return True
    return False


while True:

    try:
        print("fetching with username/passwords")
        # if username is not found, raise to goto loop B
        if "USERNAME" not in data_json["Weibo"]:
            raise Exception
        # Loop A: fetch with username/passwords
        c = Client()
        c.revoke_token()
        c.get_token()
        c.set_client()

        # while True:
        # print("token expires in: " + str(c.token_expire_date()) + " sec")
        # todo: renew token if it is about to expire
        # check fetching limits
        lim = c.get_weibo_package("account/rate_limit_status")
        print("remaining ip hits: " + str(lim["remaining_ip_hits"]))
        if lim["remaining_ip_hits"] <= 1:
            print("continue after " + str(lim["reset_time_in_seconds"]) + " seconds")
            time.sleep(lim["reset_time_in_seconds"])
        result = c.get_weibo_package("statuses/home_timeline")  # fetch posts
        if worth(result["statuses"][0]["idstr"]) is True:
            embed = Weibo2DiscordWebhook(result["statuses"][0])  # convert to discord file
            embed.post()  # post to discord
        time.sleep(sleep_time)  # limit rate of fetching from weibo = 150/hr, min=24? sec/ping

    except Exception:
        print("fetching without username/passwords")
        # loop B: fetch without username/passwords

        def convert_content(html_content):
            markdown_content = h.handle(html_content)

            try:
                content, _ = markdown_content.split("\n活动详情请阅")
            except ValueError:
                content = markdown_content
            return content

        client = WeiboClient()
        h = html2text.HTML2Text()
        h.ignore_links = True
        p = client.people('5732523783')
        hook = Webhook(data_json["Discord"]["WEBHOOK_URL"], content="test3",
                       username=str(p.name),
                       avatar=p.avatar)
        # While True:
        for status in p.statuses.page(1):
            if status.isTop is None:
                if worth(status.id):
                    hook.set_content(convert_content(status.longTextContent))
                    if status.original_pic is not None:
                        hook.set_image(status.original_pic)
                    hook.set_footer(text=u"发布时间：{}".format(status.created_at))
                    data_json["Weibo"]["LAST_WEIBO_ID"] = status.id
                    hook.post()
                break
        count = count + 1
        print(count)
        time.sleep(sleep_time)
