from PIL import Image
import os

def resize_and_crop_images(source_folder, destination_folder, target_width, target_height, crop_ratio):
    """
    Resize and crop images in a folder.

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

            # Resize image
            img_resized = img.resize((target_width, target_height))

            # Calculate crop values
            crop_height = int(crop_ratio / 100.0 * target_height)
            crop_box = (0, crop_height, target_width, target_height - crop_height)

            # Crop image
            img_cropped = img_resized.crop(crop_box)

            # Save the modified image to the destination folder
            img_cropped.save(os.path.join(destination_folder, filename))

    print(f"Images have been resized and cropped to {destination_folder}")

if __name__ == "__main__":
    # Prompt user for inputs
    source_folder = input("Enter the source folder path: ")
    destination_folder = input("Enter the destination folder path: ")
    target_width = int(input("Enter the target width (in pixels): "))
    target_height = int(input("Enter the target height (in pixels): "))
    crop_ratio = float(input("Enter the crop ratio (as a percentage): "))

    resize_and_crop_images(source_folder, destination_folder, target_width, target_height, crop_ratio)
