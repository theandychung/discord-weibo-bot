from bot.dataIO import fileIO
import os
# //           "5013723252",
try:
    data_json = {
        "Discord": {
            "webhook_url": os.environ["WEBHOOK_URL"]
        },
        "Weibo": {
            "weibo_id": os.environ["WEIBO_ID"].replace(" ", "").split(",")
        }
    }
except:
    if fileIO("bot/data.json", "check"):
        data_json = fileIO("bot/data.json", "load")
    else:
        raise ValueError("error when loading global values")
