import logging
import requests
from config import cfg

LOG_FORMAT = "%(asctime)s|%(levelname)s|%(process)d|%(module)s|%(funcName)s|%(lineno)d|%(message)s"
logging.basicConfig(level=cfg["LOG_LEVEL"], format=LOG_FORMAT, force=True)
logger = logging.getLogger(__name__)


def init_client():
    get_client_credentials()
    get_access_token()


def set_peertube_instance(url: str = cfg["PEERTUBE_PROD_URL"]):
    """Set the Peertube instance we are working with. Defaults to PROD."""
    cfg["PEERTUBE_URL"] = url


def get_client_credentials():
    """Add client credentials to config."""
    OAUTH_CLIENT_URL = f"{cfg["PEERTUBE_URL"]}/api/v1/oauth-clients/local"

    logger.info("Get client credentials...")
    logger.debug(OAUTH_CLIENT_URL)
    response = requests.get(OAUTH_CLIENT_URL)
    logger.debug(f"{response.url}")
    response.raise_for_status()
    if response.status_code == 200:
        client_data = response.json()
        cfg["CLIENT_ID"] = client_data["client_id"]
        cfg["CLIENT_SECRET"] = client_data["client_secret"]
        logger.debug("Client ID:", cfg["CLIENT_ID"])
        logger.debug("Client SECRET:", cfg["CLIENT_SECRET"])
    else:
        logger.error(
            "Failed to retrieve credentials:", response.status_code, response.text
        )


def get_access_token():
    """Get the Peertube access token and add it to the config."""
    TOKEN_URL = f"{cfg["PEERTUBE_TEST_URL"]}/api/v1/users/token"
    logger.info("Get the Peertube access token.")
    logger.debug(TOKEN_URL)

    data = {
        "client_id": cfg["CLIENT_ID"],
        "client_secret": cfg["CLIENT_SECRET"],
        "grant_type": "password",
        "username": cfg["USERNAME"],
        "password": cfg["PASSWORD"],
    }
    logger.debug(data)
    response = requests.post(TOKEN_URL, data=data)
    logger.debug(f"{response.url}")
    response.raise_for_status()
    if response.status_code == 200:
        token_data = response.json()
        cfg["TOKEN_TYPE"] = token_data["token_type"]
        cfg["ACCESS_TOKEN"] = token_data["access_token"]
        logger.debug(f"Token type: {cfg["TOKEN_TYPE"]}")
        logger.debug(f"Access Token: {cfg["ACCESS_TOKEN"]}")
        logger.debug(f"Expires In: {token_data["expires_in"]} seconds")
    else:
        logger.error("Failed to retrieve token:", response.status_code, response.text)


def get_total_videos_for_channel(channel_id: str) -> int:
    """Gets the total number of videos for a channel."""
    logger.debug("Get total number of videos for a channel.")
    total = 0
    response = requests.get(
        f"{cfg["PEERTUBE_TEST_URL"]}/api/v1/video-channels/{channel_id}/videos?count=0"
    )
    logger.debug(f"{response.url}")
    response.raise_for_status()
    if response.status_code == 200:
        videos = response.json()
        logger.debug(videos)
        total = videos["total"]
        logger.info(f"Total of {total} videos for channel '{channel_id}'.")
    else:
        logger.error(
            f"Got an {response.status_code} error from the server. Reason: {response.reason}"
        )
    return total


def get_videos_for_channel(channel_id: str):
    """Gets a list of videos for a channel."""
    logger.debug("Get a list of videos for a channel.")

    # GET videos total from channel
    total = get_total_videos_for_channel(channel_id)

    # GET videos from channel
    offset = 10
    for x in range(0, total, offset):
        response = requests.get(
            f"{cfg["PEERTUBE_TEST_URL"]}/api/v1/video-channels/{channel_id}/videos?start={x}&count={offset}&skipCount=true"
        )
        logger.debug(f"{response.url}")
        response.raise_for_status()
        if response.status_code == 200:
            videos = response.json()
            logger.debug(videos)
        else:
            logger.error(
                f"Got an {response.status_code} error from the server. Reason: {response.reason}"
            )


def get_channels():
    raise NotImplementedError


# # Authorization header
# headers = {"Authorization": f"{cfg["TOKEN_TYPE"]} {cfg["ACCESS_TOKEN"]}"}
