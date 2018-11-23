from discord_hooks import Webhook
from global_values import data_json
from weibo_api.weibo.status import Status

import html2text
"""
modified from
https://github.com/4rqm/dhooks

discord webhook documentation
https://discordapp.com/developers/docs/resources/webhook#execute-webhook
"""




# class Weibo2DiscordWebhook2(Webhook):
#     status = Status()
#     h = html2text.HTML2Text()
#     h.ignore_links = True
#
#     def __init__(self, status, **kwargs):
#         self.url = data_json["Discord"]["WEBHOOK_URL"]
#         super().__init__(self.url, **kwargs)
#         self.set_content()
#         if "original_pic" in status:
#             self.image = status["original_pic"]
#         if "user" in status:
#             self.avatar = status["user"]["avatar"]
#             self.username = status["user"]["name"]
#
#     def set_content(self):
#         # self.content = h.handle(status["longTextContent"])
#         self.content = "herehere"
#
# if __name__=="__main__":
#     hook = Weibo2DiscordWebhook2(content="there")
#     hook.post()
