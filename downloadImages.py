import os
import requests
import json


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Image saved as {filename}")
    else:
        print(f"Failed to download image from {url}")


def download_images_from_json(json_file, save_dir):
    """Load pal data from a JSON file and download images to the specified directory."""
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    with open(json_file, "r") as file:
        pal_data = json.load(file)

    for pal in pal_data:
        image_url = pal.get("imageWiki")
        key = pal.get("key")

        if image_url and key:
            filename = os.path.join(save_dir, f"{key}.png")
            download_image(image_url, filename)


json_file = "result/pals.json"

save_dir = "result/images"

download_images_from_json(json_file, save_dir)
