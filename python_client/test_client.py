import logging
import json
from config import cfg
from client_peertube import (
    setup,
    show_video_passwords,
    Privacy,
    get_channel_id,
    list_videos_for_channel,
    show_video_data,
    upload_video,
    delete_video,
    get_video,
    update_video,
    set_video_password_protected,
    list_videos_for_an_account,
    list_videos,
    get_total_videos_for_channel,
    list_videos_for_channel_privacy_one_of,
    list_videos_for_an_account_privacy_one_of,
    get_video_token,
    list_users,
    list_channels,
    get_streaming_playlist,
    get_static_video_url,
)

LOG_FORMAT = "%(asctime)s|%(levelname)s|%(process)d|%(module)s|%(funcName)s|%(lineno)d|%(message)s"
logging.basicConfig(level=cfg["LOG_LEVEL"], format=LOG_FORMAT, force=True)
logger = logging.getLogger(__name__)


def upload_video_in_channel(channel_handle: str):
    """Upload a video in a channel and make it password protected/"""
    channel_id = get_channel_id(channel_handle)
    if channel_id:
        # now add a video
        video_data = {
            "video_path": cfg["VIDEO_PATH"],
            "channelId": channel_id,
            "name": cfg["VIDEO_NAME"],
            "downloadEnabled": "false",
            "privacy": Privacy.Password_protected.value,
            "videoPasswords": [
                cfg["VIDEO_PASSWORD"],
            ],
        }
        logger.debug(video_data)
        logger.debug(json.dumps(video_data, indent=4))
        video_id = upload_video(video_data)


def list_all_videos_for_account(name: str):
    payload = list_videos_for_an_account(name)
    if payload:
        all_videos = json.loads(payload)
        logger.debug(json.dumps(all_videos, indent=2))


def list_private_videos_for_account(name: str):
    payload = list_videos_for_an_account_privacy_one_of(name, Privacy.Private.value)
    if payload:
        all_videos = json.loads(payload)
        logger.debug(json.dumps(all_videos, indent=2))


def list_password_protected_videos_for_account(name: str):
    payload = list_videos_for_an_account_privacy_one_of(
        name, Privacy.Password_protected.value
    )
    if payload:
        all_videos = json.loads(payload)
        logger.debug(json.dumps(all_videos, indent=2))


def list_all_videos_for_channel_privacy_one_of(name: str, privacy: int):
    payload = list_videos_for_channel_privacy_one_of(name, privacy=privacy)
    if payload:
        all_videos = json.loads(payload)
        logger.debug(json.dumps(all_videos, indent=2))


def list_all_videos():
    payload = list_videos()
    if payload:
        all_videos = json.loads(payload)
        logger.debug(json.dumps(all_videos, indent=2))


def show_video_metadata(video_id: int | str):
    """Shows some basic metadata for a video."""
    payload = get_video(video_id)
    if payload:
        md = json.loads(payload)
        logger.debug(json.dumps(md, indent=2))


def update_video_privacy(video_id: int | str, privacy: int) -> str:
    """Update a video privacy setting."""
    data = {
        "privacy": privacy,
    }
    return update_video(video_id, data=data)


def set_video_password(video_id: int | str, password: str) -> str:
    """Sets video password for video. Implies also setting the privacy."""
    return set_video_password_protected(video_id, password)


def remove_video_password(video_id: int | str) -> str:
    """Simple test to update a video password setting."""
    # remove it by setting none
    data = {
        "videoPasswords": [],
    }
    return update_video(video_id, data=data)


def list_all_users():
    """List all users of an instance."""
    payload = list_users()
    if payload:
        user_list = json.loads(payload)
        logger.debug(json.dumps(user_list, indent=2))


def list_all_channels():
    """List all channels of an instance."""
    payload = list_channels()
    if payload:
        channel_list = json.loads(payload)
        logger.debug(json.dumps(channel_list, indent=2))


def show_streaming_playlists(video_id: int | str):
    """Show what streaming playlist are listed"""
    payload = get_video(video_id)
    if payload:
        md = json.loads(payload)
        logger.debug(f"Video_id:{md["id"]}")
        for f in md["streamingPlaylists"]:
            if "playlistUrl" in f:
                logger.debug(f"Playlist URL: {json.dumps(f["playlistUrl"], indent=2)}")


if __name__ == "__main__":
    """Small testing script for the Peertube API."""
    logger.info("Starting test script.")
    setup(cfg["PEERTUBE_TEST_URL"])

    ## VIDEOS
    video_id = "kkwR4KndB5eejav6UbWvAn"  # willem video
    # video_id = "2xo6jhHtfnE8LzLYLDezY7" # ons_land video
    logger.debug(video_id)

    # show_video_metadata(video_id)
    # update_video_privacy(video_id, Privacy.Private.value)
    # resp = set_video_password(video_id, cfg["VIDEO_PASSWORD"])

    # ACCOUNTS
    # list_all_users()
    account = "willem"  # ons_land
    # list_password_protected_videos_for_account(account)
    # list_private_videos_for_account(account)
    # list_all_videos_for_account(account)
    # list_all_videos()

    # CHANNELS
    # list_all_channels() # ons_land,  openbeelden, themindoftheuniverse, willem_channel
    channel = "willem_channel"
    # list_all_videos_for_channel_privacy_one_of("ons_land", Privacy.Private.value)
    list_all_videos_for_channel_privacy_one_of(
        channel, Privacy.Password_protected.value
    )
    # list_videos_for_channel(channel)

    # VIDEO TOKENS
    # show_streaming_playlists(video_id)

    # stat_video_url = get_static_video_url(video_id)
    # logger.debug(stat_video_url)

    # all_videos = list_videos_for_channel(channel)
    # for v in all_videos:
    #     set_video_password_protected(v["shortUUID"], cfg["VIDEO_PASSWORD"])
