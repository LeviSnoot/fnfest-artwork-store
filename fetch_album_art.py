import requests
import os
import json
import time

API_URL = "https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game/spark-tracks"
IMAGE_DIR = "album_art"

def fetch_album_art_urls():
    print("Fetching album art URLs...")
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    
    # Extract album art URLs from the data
    album_art_urls = []
    for track_id, track_data in data.items():
        if isinstance(track_data, dict) and "track" in track_data:
            album_art_url = track_data["track"].get("au")
            if album_art_url:
                album_art_urls.append(album_art_url)
    
    print(f"Found {len(album_art_urls)} album art URLs.")
    return album_art_urls

def download_images(urls):
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    
    total_images = len(urls)
    for index, url in enumerate(urls):
        image_name = os.path.basename(url)
        image_path = os.path.join(IMAGE_DIR, image_name)
        
        if not os.path.exists(image_path):
            print(f"Downloading {image_name} ({index + 1}/{total_images})...")
            response = requests.get(url)
            response.raise_for_status()
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {image_name} ({index + 1}/{total_images})")
            time.sleep(5)  # Wait for 5 seconds between downloads

if __name__ == "__main__":
    album_art_urls = fetch_album_art_urls()
    download_images(album_art_urls)
    print("All images downloaded.")
