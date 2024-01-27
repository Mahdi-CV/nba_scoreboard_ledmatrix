import os
import sys
from PIL import Image

def resize_images(image_directory, target_size):
    for filename in os.listdir(image_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(image_directory, filename)
            with Image.open(file_path) as img:
                img = img.resize((target_size, target_size))
                img.save(file_path)
            print(f"Resized {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_images> <target_size>")
        sys.exit(1)

    image_directory = sys.argv[1]
    target_size = int(sys.argv[2])

    resize_images(image_directory, target_size)
