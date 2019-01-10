from bot.dataIO import fileIO
import os

if fileIO("bot/data.json", "check"):
    data_json = fileIO("bot/data.json", "load")
else:
    data_json = {
        "Discord": {
            "webhook_url": os.environ["WEBHOOK_URL"]
        },
        "Weibo": {
            "weibo_id": os.environ["WEIBO_ID"].replace(" ", "").split(",")
        }
    }

if data_json["Weibo"]["weibo_id"] is "" or None:
    raise ValueError("weibo id not found")
