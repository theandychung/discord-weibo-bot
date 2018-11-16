from discord_hooks import Webhook
from globalv import data_json
"""
modified from
https://github.com/4rqm/dhooks

discord webhook documentation
https://discordapp.com/developers/docs/resources/webhook#execute-webhook
"""


class Weibo2DiscordWebhook(Webhook):
    weibo_statuses = {}

    def __init__(self, weibo_statuses, **kwargs):
        self.url = data_json["Discord"]["WEBHOOK_URL"]
        super().__init__(self.url, **kwargs)
        if "text" in weibo_statuses:
            self.content = weibo_statuses["text"]
        if 'user' in weibo_statuses:
            self.username = weibo_statuses["user"]["name"]
            self.avatar = weibo_statuses["user"]["profile_image_url"]
        if "original_pic" in weibo_statuses:
            self.image = weibo_statuses["original_pic"]
        if "created_at" in weibo_statuses:
            self.footer = "Created at: " + weibo_statuses["created_at"]
            self.ts = False


