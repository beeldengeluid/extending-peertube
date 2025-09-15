import logging
import requests
from pathlib import Path
from enum import Enum
from urllib.parse import urlencode
import json
from config import cfg

LOG_FORMAT = "%(asctime)s|%(levelname)s|%(process)d|%(module)s|%(funcName)s|%(lineno)d|%(message)s"
logging.basicConfig(level=cfg["LOG_LEVEL"], format=LOG_FORMAT, force=True)
logger = logging.getLogger(__name__)


class Privacy(Enum):
    """
    Public: your video is public. Everyone can see it (by using search engine, link or embed);
    Internal: only authenticated user having an account on your PeerTube platform can see your video. Users searching from another PeerTube platform or having the link without being authentifaced can't see it;
    Unlisted: only people with the private link can see this video; the video is not visible without its link (can't be found by searching);
    Private: only you can see the video;
    Password protected: only users with the appropriate password can see this video; PeerTube >= 6.0
    """

    Public = 1
    Unlisted = 2
    Private = 3
    Internal = 4
    Password_protected = 5


def init_client():
    get_client_credentials()
    get_access_token()


def set_peertube_instance(url: str = cfg["PEERTUBE_PROD_URL"]):
    """Set the Peertube instance we are working with. Defaults to PROD."""
    cfg["PEERTUBE_URL"] = url


def get_client_credentials():
    """Add client credentials to config."""
    logger.info("Get client credentials...")
    try:
        # API URL
        OAUTH_CLIENT_URL = f"{cfg["PEERTUBE_URL"]}/api/v1/oauth-clients/local"
        logger.debug(OAUTH_CLIENT_URL)

        # do request
        response = requests.get(OAUTH_CLIENT_URL)
        logger.debug(f"{response.url}")
        client_data = response.json()
        logger.debug(client_data)
        response.raise_for_status()
        cfg["CLIENT_ID"] = client_data["client_id"]
        cfg["CLIENT_SECRET"] = client_data["client_secret"]
    except requests.HTTPError as e:
        logger.error(f"Status: {e.response.status_code} Reason: {e.response.reason}")
    except Exception as e:
        logger.error(f"Failed to retrieve credentials: {str(e)}")


def get_access_token():
    """Get the Peertube access token and add it to the config."""
    logger.info("Get the Peertube access token.")
    try:
        TOKEN_URL = f"{cfg["PEERTUBE_URL"]}/api/v1/users/token"
        logger.debug(TOKEN_URL)

        # data
        data = {
            "client_id": cfg["CLIENT_ID"],
            "client_secret": cfg["CLIENT_SECRET"],
            "grant_type": "password",
            "username": cfg["USERNAME"],
            "password": cfg["PASSWORD"],
        }
        logger.debug(data)

        # do request
        response = requests.post(TOKEN_URL, data=data)
        logger.debug(f"{response.url}")
        token_data = response.json()
        logger.debug(token_data)
        response.raise_for_status()
        cfg["TOKEN_TYPE"] = token_data["token_type"]
        cfg["ACCESS_TOKEN"] = token_data["access_token"]
    except requests.HTTPError as e:
        logger.error(f"Status: {e.response.status_code} Reason: {e.response.reason}")
    except Exception as e:
        logger.error(f"Failed to retrieve token: {str(e)}")


def setup(peertube_instance: str = cfg["PEERTUBE_TEST_URL"]):
    """Request access tokens and client id. Store these in the config object."""
    set_peertube_instance(peertube_instance)
    init_client()


def get_total_videos_for_channel(channel_handle: str, privacy_one_of: int) -> int:
    """Gets the total number of videos for a channel."""
    logger.debug("Get total number of videos for a channel.")
    total = 0
    api_path = f"/api/v1/video-channels/{channel_handle}/videos"
    params = {
        "privacyOneOf": privacy_one_of,
    }
    payload = peertube_get(api_path, params=params)
    if payload:
        videos = json.loads(payload)
        total = videos["total"]
        logger.info(f"Total of {total} videos for channel '{channel_handle}'.")
    return total


def list_videos_for_channel(
    channel_handle: str, privacy: int = Privacy.Public.value
) -> list:
    """Gets a list of videos for a channel."""
    logger.debug("Get a list of videos for a channel.")
    all_videos = []

    # GET videos total from channel
    total = get_total_videos_for_channel(
        channel_handle,
        privacy,
    )
    offset = 10
    for x in range(0, total, offset):
        params = {"start": x, "count": offset, "privacyOneOf": privacy}
        payload = peertube_get(
            f"/api/v1/video-channels/{channel_handle}/videos",
            params=params,
        )
        videos = json.loads(payload)
        for video in videos["data"]:
            video["static_video_url"] = get_static_video_url(video["shortUUID"])
            # logger.debug(
            #     f"Video: {video["shortUUID"]} static_video_url:{video["static_video_url"]}"
            # )
        # logger.debug(videos)
        all_videos.extend(videos["data"])
    return all_videos


def get_streaming_playlist(video_id: int | str) -> str:
    """Returns the streaming playlist URL."""
    playlist_url = ""
    payload = get_video(video_id)
    if payload:
        md = json.loads(payload)
        if len(md["streamingPlaylists"]) > 1:
            logger.debug("More than one straming playlist. Please redesign function")
        f = md["streamingPlaylists"][0]
        playlist_url = f["playlistUrl"]
    return playlist_url


def get_static_video_url(video_id: int | str) -> str:
    """Gets the static URL for a video including video password."""
    playlist_URL = get_streaming_playlist(video_id)
    video_token = get_video_token(video_id)
    static_video_url = ""
    if video_token:
        params = {"videoFileToken": video_token, "reinjectVideoFileToken": 1}
        logger.debug(f"Params: {urlencode(params)}")
        static_video_url = f"{playlist_URL}?{urlencode(params)}"
    return static_video_url


def get_channel_id(channel_handle: str) -> int:
    """Get the channel id using the channel name."""
    logger.debug("Get the channel id using the channel name.")
    channel_id = 0
    api_path = f"/api/v1/video-channels/{channel_handle}"
    payload = peertube_get(api_path)
    resp = json.loads(payload)
    channel_id = resp["id"]
    logger.info(f"The channel_id for channel '{channel_handle}' is {channel_id}.")
    return channel_id


def upload_video(video_data: dict) -> int:
    """Upload video and metadata to Peertube."""
    logger.info("Upload video and metadata to Peertube.")
    video_id = 0
    try:
        UPLOAD_URL = f"{cfg["PEERTUBE_URL"]}/api/v1/videos/upload"
        logger.debug(UPLOAD_URL)
        video = Path(video_data["video_path"])
        del video_data["video_path"]  # we don't need that anymore
        headers = {"Authorization": f"{cfg["TOKEN_TYPE"]} {cfg["ACCESS_TOKEN"]}"}
        logger.debug(headers)
        logger.debug(video_data)
        mime_type = "video/mp4"
        with open(str(video.resolve()), "rb") as video_file:
            files = {
                "videofile": (
                    video.resolve().name,
                    video_file,
                    mime_type,
                )
            }
            logger.debug(
                f"File tuple: {files['videofile'][0]}, MIME type: {files['videofile'][2]}"
            )
            response = requests.post(
                UPLOAD_URL, headers=headers, files=files, data=video_data
            )

        logger.debug(f"{response.url}")
        upload_resp = response.json()
        logger.debug(upload_resp)
        response.raise_for_status()
        video_id = upload_resp["video"]["id"]
        logger.info(f"New video uploaded with video id: {video_id}")
        return video_id
    except requests.HTTPError as e:
        logger.error(f"Status: {e.response.status_code} Reason: {e.response.reason}")
    except Exception as e:
        logger.error(f"Failed to upload video: {str(e)}")
    return video_id


def delete_video(video_id: int) -> str:
    """Delete the video from Peertube."""
    logger.info("Delete video from Peertube.")
    api_path = f"/api/v1/videos/{video_id}"
    return peertube_delete(api_path)


def get_video(video_id: int | str) -> str:
    """Gets the metadata for a video."""
    logger.info("Gets video metadata.")
    api_path = f"/api/v1/videos/{video_id}"
    return peertube_get(api_path)


def show_video_data(all_videos: list):
    """Simple printing function to show the video data."""
    for video in all_videos:
        logger.info(
            f"Title: {video["name"]} URL: {video["url"]} ID: {video["id"]} Privacy: {video["privacy"]}"
        )
        logger.debug(video)


def show_video_description(video_id: int | str):
    """Shows the complete video description."""
    # https://peertube2.cpy.re/api/v1/videos/{id}/description
    raise NotImplementedError


def show_video_passwords(video_id: int | str):
    """Display the password set for the video."""
    logger.info("Show video passwords.")
    api_path = f"/api/v1/videos/{video_id}/passwords"
    payload = peertube_get(api_path)
    response = json.loads(payload)
    video_passwords = response.json()["data"]
    logger.info(f"Passwords for video with id: {video_id}: {video_passwords}")


def update_video(video_id: int | str, data: dict) -> str:
    """Updates the metadata for a video."""
    logger.info("Update video metadata.")
    api_path = f"/api/v1/videos/{video_id}"

    # headers["x-peertube-video-password"] = (
    #     "testingpeertube"  # cfg["VIDEO_PASSWORD"]
    # )

    # make the data multipart/form-data
    # NOTE: This may fail for arrays, so not a generic solution
    logger.debug(data.items())
    data = {k: (None, v) for k, v in data.items()}
    logger.debug(json.dumps(data, indent=2))
    return peertube_put(api_path, data=data)


def set_video_password_protected(video_id: int | str, password: str = "") -> str:
    """Make a video password protected and set video password."""
    logger.info("Make a video password protected and set video password.")
    api_path = f"/api/v1/videos/{video_id}"
    if password == "":
        logger.error("Video password is empty string. Needs to be set.")
        return ""
    data = {
        "videoPasswords": [
            (
                None,
                password,
            )
        ],
        "privacy": (None, f"{Privacy.Password_protected.value}"),
    }
    return peertube_put(api_path, data=data)


def get_video_token(video_id: int | str) -> str:
    """Returns the video token for a password protected video."""
    logger.info("Get video token for a password protected video.")
    api_path = f"/api/v1/videos/{video_id}/token"
    headers = {"x-peertube-video-password": cfg["VIDEO_PASSWORD"]}
    video_token = ""
    payload = peertube_post(api_path, headers=headers)
    if payload:
        data = json.loads(payload)
        video_token = data["files"]["token"]
    return video_token


def list_videos() -> str:
    """List all videos."""
    logger.info("List all videos for user.")
    api_path = f"/api/v1/videos/"
    return peertube_get(api_path)


def list_videos_for_an_account(name: str) -> str:
    """List all videos for an account."""
    logger.info(f"List videos for account with name '{name}'.")
    api_path = f"/api/v1/accounts/{name}/videos"
    return peertube_get(api_path)

    # return list_videos_for_an_account_privacy_one_of(name)


def list_videos_for_an_account_privacy_one_of(
    name: str, privacy: int = Privacy.Public.value
) -> str:
    """List all videos for an account taking privacy param."""
    logger.info(f"List {Privacy(privacy)} videos for account with name '{name}'.")
    api_path = f"/api/v1/accounts/{name}/videos"
    params = {"privacyOneOf": privacy}
    return peertube_get(api_path, params=params)


def list_videos_for_channel_privacy_one_of(name: str, privacy: int = 1) -> str:
    """List videos for an channel taking privacy setting."""
    logger.info(f"List videos for channel '{name}'.")
    api_path = f"/api/v1/video-channels/{name}/videos"
    params = {"privacyOneOf": privacy}
    return peertube_get(api_path, params=params)


def list_users() -> str:
    """List users"""
    logger.info(f"List users.")
    api_path = f"/api/v1/users"
    return peertube_get(api_path)


def list_channels() -> str:
    """List channels"""
    logger.info(f"List users.")
    api_path = f"/api/v1/video-channels"
    return peertube_get(api_path)


def peertube_get(url_path: str = "", headers: dict = {}, params: dict = {}) -> str:
    """Generic get request, taking url path, header and params. Return response as text.
    Note: can not be used on 'get_client_credentials'.
    """
    try:
        API_URL = f"{cfg["PEERTUBE_URL"]}{url_path}"
        logger.debug(API_URL)

        # Authorization header
        headers.update({"Authorization": f"{cfg["TOKEN_TYPE"]} {cfg["ACCESS_TOKEN"]}"})
        logger.debug(headers)
        logger.debug(json.dumps(headers, indent=2))

        # do request
        response = requests.get(API_URL, headers=headers, params=params)
        logger.debug(f"{response.url}")
        # logger.debug(f"{response.text}")
        response.raise_for_status()
        return response.text
    except requests.HTTPError as e:
        logger.error(f"Status: {e.response.status_code} Reason: {e.response.reason}")
    except Exception as e:
        logger.error(f"Failed GET request. {str(e)}")
    return ""


def peertube_put(url_path: str = "", headers: dict = {}, data: dict = {}) -> str:
    """Sends a put request to peertube+url_path, taking headers and data. Returns the response."""
    try:
        API_URL = f"{cfg["PEERTUBE_URL"]}{url_path}"
        logger.debug(API_URL)
        headers.update({"Authorization": f"{cfg["TOKEN_TYPE"]} {cfg["ACCESS_TOKEN"]}"})
        logger.debug(json.dumps(headers, indent=2))
        response = requests.put(API_URL, headers=headers, data=data)
        logger.debug(f"{response.url}")
        # logger.debug(f"{response.text}")
        response.raise_for_status()
        return response.text
    except requests.HTTPError as e:
        logger.error(f"Status: {e.response.status_code} Reason: {e.response.reason}")
    except Exception as e:
        logger.error(f"Failed PUT request. {str(e)}")
    return ""


def peertube_post(url_path: str = "", headers: dict = {}, data: dict = {}) -> str:
    """Sends a put request to peertube+url_path, taking headers and data. Returns the response.
    Note that this can not be used to get the access token.
    """
    try:
        API_URL = f"{cfg["PEERTUBE_URL"]}{url_path}"
        logger.debug(API_URL)
        headers.update({"Authorization": f"{cfg["TOKEN_TYPE"]} {cfg["ACCESS_TOKEN"]}"})
        logger.debug(json.dumps(headers, indent=2))
        response = requests.post(API_URL, headers=headers, data=data)
        logger.debug(f"{response.url}")
        # logger.debug(f"{response.text}")
        response.raise_for_status()
        return response.text
    except requests.HTTPError as e:
        logger.error(f"Status: {e.response.status_code} Reason: {e.response.reason}")
    except Exception as e:
        logger.error(f"Failed POST request. {str(e)}")
    return ""


def peertube_delete(url_path: str = "", headers: dict = {}) -> str:
    """Sends a delete request to peertube+url_path. Returns the response."""
    try:
        API_URL = f"{cfg["PEERTUBE_URL"]}{url_path}"
        logger.debug(API_URL)

        # Authorization header
        headers.update({"Authorization": f"{cfg["TOKEN_TYPE"]} {cfg["ACCESS_TOKEN"]}"})
        logger.debug(json.dumps(headers, indent=2))

        # do request
        response = requests.delete(API_URL, headers=headers)
        logger.debug(f"{response.url}")
        # logger.debug(f"{response.text}")
        response.raise_for_status()
        return response.text
    except requests.HTTPError as e:
        logger.error(f"Status: {e.response.status_code} Reason: {e.response.reason}")
    except Exception as e:
        logger.error(f"Failed DELETE request. {str(e)}")
    return ""
