import logging
from config import cfg
from client_peertube import (
    set_peertube_instance,
    init_client,
    get_videos_for_channel,
)

LOG_FORMAT = "%(asctime)s|%(levelname)s|%(process)d|%(module)s|%(funcName)s|%(lineno)d|%(message)s"
logging.basicConfig(level=cfg["LOG_LEVEL"], format=LOG_FORMAT, force=True)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    """Small testing script for the Peertube API."""
    logger.info("Starting the channel manager test script.")
    set_peertube_instance(cfg["PEERTUBE_TEST_URL"])
    init_client()
    get_videos_for_channel(cfg["PEERTUBE_CHANNEL"])
