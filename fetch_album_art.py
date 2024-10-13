import requests
import os
import time

API_URL = "https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game/spark-tracks"
IMAGE_DIR = "album_art"
THUMBNAIL_DIR = "thumbnails"

def fetch_album_art_urls():
    print("Fetching album art and thumbnail URLs...")
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    
    album_art_urls = []
    thumbnail_urls = []
    for track_id, track_data in data.items():
        if isinstance(track_data, dict) and "track" in track_data:
            album_art_url = track_data["track"].get("au")
            thumbnail_url = track_data["track"].get("tb")
            if album_art_url:
                album_art_urls.append(album_art_url)
            if thumbnail_url:
                thumbnail_urls.append(thumbnail_url)
    
    print(f"Found {len(album_art_urls)} album art URLs and {len(thumbnail_urls)} thumbnail URLs.")
    return album_art_urls, thumbnail_urls

def download_images(urls, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    total_images = len(urls)
    for index, url in enumerate(urls):
        image_name = os.path.basename(url)
        image_path = os.path.join(directory, image_name)
        
        if not os.path.exists(image_path):
            print(f"Downloading {image_name} ({index + 1}/{total_images}) to {directory}...")
            response = requests.get(url)
            response.raise_for_status()
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {image_name} ({index + 1}/{total_images}) to {directory}")
            time.sleep(3)  # Wait for 3 seconds between downloads

if __name__ == "__main__":
    album_art_urls, thumbnail_urls = fetch_album_art_urls()
    download_images(album_art_urls, IMAGE_DIR)
    download_images(thumbnail_urls, THUMBNAIL_DIR)
    print("All images and thumbnails downloaded.")