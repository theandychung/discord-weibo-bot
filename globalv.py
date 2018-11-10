from dataIO import fileIO
import os

if fileIO("data.json", "check"):
    data_json = fileIO("data.json", "load")
else:
    data_json = {
        "Discord": {
            "WEBHOOK_URL": os.environ["WEBHOOK_URL"]
        },
        "Weibo": {
            "ACCESS_TOKEN": os.environ["ACCESS_TOKEN"],
            "APP_KEY": os.environ["APP_KEY"],
            "APP_SECRET": os.environ["APP_SECRET"],
            "LAST_WEIBO_ID": os.environ["LAST_WEIBO_ID"],
            "PASSWORDS": os.environ["PASSWORDS"],
            "REDIRECT_URL": os.environ["REDIRECT_URL"],
            "USERNAME": os.environ["USERNAME"]
        }
    }