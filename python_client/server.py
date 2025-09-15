import logging
from flask import Flask, render_template
from flask import request, Response

# import requests
# import json
from config import cfg
from client_peertube import (
    set_peertube_instance,
    init_client,
    Privacy,
    list_videos_for_channel,
)

LOG_FORMAT = "%(asctime)s|%(levelname)s|%(process)d|%(module)s|%(funcName)s|%(lineno)d|%(message)s"
logging.basicConfig(level=cfg["LOG_LEVEL"], format=LOG_FORMAT, force=True)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config.update(
    APP_HOST=cfg["FLASK"]["APP_HOST"], APP_PORT=cfg["FLASK"]["APP_PORT"], DEBUG=True
)

set_peertube_instance(cfg["PEERTUBE_TEST_URL"])
init_client()


@app.route("/")
def homepage():
    title = "Peertube video token demo"
    paragraph = ["The amazing video token demo using B&G Peertube!"]
    videos = list_videos_for_channel(
        cfg["PEERTUBE_CHANNEL"], privacy=Privacy.Password_protected.value
    )
    for v in videos:
        logger.debug(f"{v['shortUUID']} {v['static_video_url']}")
    try:
        return render_template(
            "index.html", title=title, paragraph=paragraph, all_videos=videos
        )
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host=app.config.get("APP_HOST"), port=app.config.get("APP_PORT"))
