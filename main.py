from dhooks import Webhook, Embed
from global_values import data_json
from weibo_api.weibo_api.client import WeiboClient
import html2text
import re
from proxy import IPPool
import time

# init
sleep_time = 3
last_weibo_id = {}
first_run_send = True  # false
use_proxy = True

def worth(user_id, post_id):
    """check worthy to post"""
    user_id = str(user_id)
    post_id = str(post_id)
    if user_id not in last_weibo_id:
        last_weibo_id.update({user_id: post_id})
        if first_run_send:
            return True
    else:
        if last_weibo_id.get(user_id) != post_id:
            last_weibo_id[user_id] = post_id
            return True
    return False


def convert_content(html_content):
    if 'http' in html_content:
        html_content = re.sub(r'(.*)(<br\s*/>.*)(<br\s*/>.*)', r'\1\n', html_content)
    markdown_content = h.handle(html_content)
    # print(markdown_content)
    return markdown_content


hook = Webhook(data_json["Discord"]["webhook_url"])

if use_proxy == True:
    proxy = IPPool().get_sslproxies_ip
else:
    proxy = None

while True:
    try:
        # print("fetching without username/passwords")
        # loop B: fetch without username/passwords
        client = WeiboClient(proxies=proxy)
        h = html2text.HTML2Text()
        h.ignore_links = True
        for za_id in data_json["Weibo"]["weibo_id"]:
            p = client.people(za_id)
            for status in p.statuses.page(1):
                if status.isTop is None:
                    if worth(za_id, status.id):
                        embed = None
                        if status.original_pic is not None:
                            embed = Embed(image_url=status.original_pic)
                        # hook.send(convert_content(status.longTextContent),
                        #           username=p.name,
                        #           avatar_url=p.avatar,
                        #           embed=embed)
                        print("sent")
                    break
        time.sleep(sleep_time)
    except ConnectionError as e:
        print(e)
        print("get new ip")
        if use_proxy == True:
            proxy = IPPool().get_sslproxies_ip
        else:
            proxy = None

    except Exception:
        break