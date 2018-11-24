import re
from weibo_api.weibo_api.client import WeiboClient
import html2text
from global_values import data_json
from dhooks import Webhook
import time

first_run_send = True  # false
last_weibo_id = {}


def worth(user_id, post_id):
    """
    check worthy to post
    """
    if user_id is None:
        user_id = ""
    if user_id not in last_weibo_id:
        last_weibo_id.update({user_id: post_id})
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


client = WeiboClient()
h = html2text.HTML2Text()
h.ignore_links = True


weibo_id = ['5732523783', '5013723252']
b = weibo_id
print(b)