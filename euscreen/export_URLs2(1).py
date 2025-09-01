import requests
import time
import csv

PEERTUBE_URL = "https://peertube.beeldengeluid.nl"
PLAYLIST_ID = "fJJ891VyCs2jXSY2PQG1tR"
PEERTUBE_TOKEN = "d6567c034ce8cf8a9df65fb7b159f91a727788f4"
HEADERS = {"Authorization": f"Bearer {PEERTUBE_TOKEN}"}

MAX_RETRIES = 5
MAX_PAGES = 10
OUTPUT_CSV = "video_urls.json"

def fetch_playlist_videos(playlist_id):
    all_videos = []
    for page in range(1, MAX_PAGES + 1):
        url = f"{PEERTUBE_URL}/api/v1/video-playlists/{playlist_id}/videos?page={page}&count=50"
        print(f"\n🔍 Fetching page {page}: {url}")
        
        retries = 0
        while retries < MAX_RETRIES:
            try:
                response = requests.get(url, headers=HEADERS, timeout=10)
                
                if response.status_code == 429:
                    wait_time = 2 ** retries
                    print(f"⚠️  Rate limited (429). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    retries += 1
                    continue
                
                if response.status_code != 200:
                    print(f"❌ Failed with status code: {response.status_code}")
                    print(f"Details: {response.text}")
                    return all_videos

                data = response.json().get("data", [])
                if not data:
                    print("ℹ️ No more videos found on this page.")
                    return all_videos

                all_videos.extend(data)
                break  # Success: exit retry loop

            except requests.exceptions.RequestException as e:
                wait_time = 2 ** retries
                print(f"❌ Request failed: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                retries += 1

    return all_videos


def save_video_urls_to_json(videos, filename):
    urls = [f"{PEERTUBE_URL}/w/{v['video']['uuid']}" for v in videos if 'video' in v and 'uuid' in v['video']]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Video URL"])
        for url in urls:
            writer.writerow([url])
    print(f"\n💾 Saved {len(urls)} URLs to {filename}")


# === MAIN EXECUTION ===

print(f"\n🎬 Fetching videos from playlist ID: {PLAYLIST_ID}")
videos = fetch_playlist_videos(PLAYLIST_ID)

if videos:
    print(f"\n✅ Found {len(videos)} video(s). Saving to file...")
    save_video_urls_to_json(videos, "video_urls.json")
else:
    print("⚠️ No videos found or all requests failed.")
