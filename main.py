from dhooks import Webhook
from global_values import data_json
from weibo_api.weibo_api.client import WeiboClient
import html2text
from my_weibo_api.weiboclient import Client
import re

# init
count = 0
sleep_time = 200
last_weibo_id = {}

first_run_send = False  # false


def worth(user_id, post_id):
    """check worthy to post"""
    user_id = str(user_id)
    post_id = str(post_id)
    if user_id not in data_json["Weibo"]["weibo_id"]\
            and data_json["Weibo"]["weibo_id"] != []:
        return False
    if user_id not in last_weibo_id:
        last_weibo_id.update({user_id: post_id})
        if first_run_send:
            return True
    else:
        if last_weibo_id.get(user_id) != post_id:
            last_weibo_id[user_id] = post_id
            return True
    return False


c = Client()
# c.revoke_token()
c.get_token()
c.set_client()
while True:

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
                    # hook.post()
                    print("sent")
                break

