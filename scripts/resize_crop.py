import sys
from PIL import Image
import os

def resize_and_crop_images(source_folder, destination_folder, target_width, target_height, crop_ratio):
    """
    Crop and resize images in a folder.

    Parameters:
    - source_folder: Path to the source folder containing images.
    - destination_folder: Path to the destination folder to save modified images.
    - target_width: The target width for the resized images.
    - target_height: The target height for the resized images.
    - crop_ratio: Percentage of the image to crop vertically from the top and bottom.
    """
    # Ensure destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(source_folder, filename)
            img = Image.open(img_path)

            # Original dimensions
            orig_width, orig_height = img.size

            # Calculate crop values
            crop_height = int(crop_ratio / 100.0 * orig_height)
            crop_box = (0, crop_height // 2, orig_width, orig_height - (crop_height // 2))

            # Crop image
            img_cropped = img.crop(crop_box)

            # Resize image
            img_resized = img_cropped.resize((target_width, target_height))

            # Save the modified image to the destination folder
            img_resized.save(os.path.join(destination_folder, filename))

    print(f"Images have been cropped and resized to {destination_folder}")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py source_folder destination_folder target_width target_height crop_ratio")
        sys.exit(1)
    
    source_folder = sys.argv[1]
    destination_folder = sys.argv[2]
    target_width = int(sys.argv[3])
    target_height = int(sys.argv[4])
    crop_ratio = float(sys.argv[5])

    resize_and_crop_images(source_folder, destination_folder, target_width, target_height, crop_ratio)
