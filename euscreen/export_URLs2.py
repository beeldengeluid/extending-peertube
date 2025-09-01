import requests
import time
import json

# === CONFIGURATION ===
PEERTUBE_URL = "https://peertube.beeldengeluid.nl"
PLAYLIST_ID = "fJJ891VyCs2jXSY2PQG1tR"
PEERTUBE_TOKEN = "d6567c034ce8cf8a9df65fb7b159f91a727788f4"
OUTPUT_FILE = "video_urls.json"

HEADERS = {
    "Authorization": f"Bearer {PEERTUBE_TOKEN}",
    "Accept": "application/json"
}

MAX_RETRIES = 5
MAX_PAGES = 20
REQUEST_DELAY = 1  # seconds between pages


def fetch_playlist_videos(playlist_id):
    all_videos = []
    for page in range(1, MAX_PAGES + 1):
        url = f"{PEERTUBE_URL}/api/v1/video-playlists/{playlist_id}/videos?page={page}&count=50"
        print(f"🔍 Fetching page {page}...")

        retries = 0
        while retries < MAX_RETRIES:
            try:
                response = requests.get(url, headers=HEADERS, timeout=10)

                if response.status_code == 429:
                    wait_time = 2 ** retries
                    print(f"⏳ Rate limited (429). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    retries += 1
                    continue

                if response.status_code != 200:
                    print(f"❌ Failed with status code: {response.status_code}")
                    print(response.text)
                    return all_videos

                data = response.json().get("data", [])
                if not data:
                    print("ℹ️ No more videos found.")
                    return all_videos

                all_videos.extend(data)
                time.sleep(REQUEST_DELAY)
                break  # success: move to next page

            except requests.exceptions.RequestException as e:
                wait_time = 2 ** retries
                print(f"⚠️ Request error: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                retries += 1

    return all_videos


def save_video_urls_to_json(videos, filename):
    seen_uuids = set()
    output = []

    for v in videos:
        video = v.get("video")
        if not video:
            continue

        uuid = video.get("uuid")
        if not uuid or uuid in seen_uuids:
            continue

        seen_uuids.add(uuid)
        output.append({
            "url": f"{PEERTUBE_URL}/w/{uuid}",
            "title": video.get("name", "Untitled"),
            "channel": video.get("channel", {}).get("name", "Unknown")
        })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Saved {len(output)} unique video(s) to {filename}")


# === MAIN ===

print(f"\n🎬 Fetching videos from playlist: {PLAYLIST_ID}")
videos = fetch_playlist_videos(PLAYLIST_ID)

if videos:
    print(f"\n✅ Found {len(videos)} total video entries. Cleaning up...")
    save_video_urls_to_json(videos, OUTPUT_FILE)
else:
    print("⚠️ No videos found or all requests failed.")
