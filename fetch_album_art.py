import requests
import os
import json
import time

API_URL = "https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game/spark-tracks"
IMAGE_DIR = "album_art"

def fetch_album_art_urls():
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
    
    return album_art_urls

def download_images(urls):
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    
    for url in urls:
        image_name = os.path.basename(url)
        image_path = os.path.join(IMAGE_DIR, image_name)
        
        if not os.path.exists(image_path):
            response = requests.get(url)
            response.raise_for_status()
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {image_name}")
            time.sleep(5)  # Wait for 5 seconds between downloads

if __name__ == "__main__":
    album_art_urls = fetch_album_art_urls()
    download_images(album_art_urls)
