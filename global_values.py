from dataIO import fileIO
import os

if fileIO("data.json", "check"):
    data_json = fileIO("data.json", "load")
else:
    data_json = {
        "Discord": {
            "webhook_url": os.environ["WEBHOOK_URL"]
        },
        "Weibo": {
            "app_key": os.environ["APP_KEY"],
            "app_secret": os.environ["APP_SECRET"],
            "passwords": os.environ["PASSWORDS"],
            "redirect_url": os.environ["REDIRECT_URL"],
            "username": os.environ["USERNAME"],
            "weibo_id": os.environ["WEIBO_ID"].replace(" ", "").split(",")
        }
    }

if data_json["Weibo"]["weibo_id"] is "" or None:
    raise ValueError("weibo id not found")
