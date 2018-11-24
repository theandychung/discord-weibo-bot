from dhooks import Webhook, Embed
from global_values import data_json
from weibo_api.weibo_api.client import WeiboClient
import time
import html2text
from my_weibo_api.weiboclient import Client
from my_weibo_api.weibo2discordwebhook import Weibo2DiscordWebhook
import re

# init
count = 0
sleep_time = 200
last_weibo_id = {}

skip_loopA = True  # true
looping = True  # true
first_run_send = False  # false


def worth(user_id, post_id):
    """check worthy to post"""
    if user_id not in last_weibo_id:
        last_weibo_id.update({user_id: post_id})
        if first_run_send:
            return True
    else:
        if last_weibo_id.get(user_id) != post_id:
            last_weibo_id[user_id] = post_id
            return True
    return False


while True:
    try:
        if skip_loopA is True:
            raise Exception
        # print("fetching with username/passwords")
        # if username is not found, raise to goto loop B
        if "username" not in data_json["Weibo"]:
            raise Exception
        # Loop A: fetch with username/passwords
        c = Client()
        # c.revoke_token()
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
        if worth("", result["statuses"][0]["idstr"]) is True:
            embed = Weibo2DiscordWebhook(result["statuses"][0])  # convert to discord file
            embed.post()  # post to discord
        time.sleep(sleep_time)  # limit rate of fetching from weibo = 150/hr, min=24? sec/ping

        if looping is False:
            break

    except Exception:
        # print("fetching without username/passwords")
        # loop B: fetch without username/passwords

        def convert_content(html_content):
            if 'http' in html_content:
                html_content = re.sub(r'(.*)(<br\s*/>.*)(<br\s*/>.*)', r'\1\n', html_content)
            markdown_content = h.handle(html_content)
            # print(markdown_content)
            return markdown_content

        client = WeiboClient()
        h = html2text.HTML2Text()
        h.ignore_links = True

        for za_id in data_json["Weibo"]["weibo_id"]:
            p = client.people(za_id)
            hook = Webhook(data_json["Discord"]["webhook_url"],
                           content="Something went wrong, please contact the developer!",
                           username=p.name,
                           avatar=p.avatar)

            for status in p.statuses.page(1):
                if status.isTop is None:
                    if worth(za_id, status.id):
                        hook.set_content(convert_content(status.longTextContent))
                        if status.original_pic is not None:
                            hook.set_image(status.original_pic)
                        # hook.set_footer(text=u"发布时间：{}".format(status.created_at))
                        hook.post()
                    break

        if looping is False:
            break
        else:
            # print(count)
            None if count is 0 else time.sleep(sleep_time)  # init loop no sleep
            # count = count + 1