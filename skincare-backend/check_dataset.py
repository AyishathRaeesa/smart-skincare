import os
from PIL import Image

folder = "C:/Users/AYSHA/OneDrive/Desktop/smart-skincare/skincare-backend/data/train"
broken_files = []
non_image_files = []

image_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}

for root, _, files in os.walk(folder):
    for file in files:
        path = os.path.join(root, file)
        ext = os.path.splitext(file)[1].lower()
        if ext not in image_exts:
            non_image_files.append(path)
            continue
        try:
            img = Image.open(path)
            img.verify()  # Checks if it's a valid image
        except Exception:
            broken_files.append(path)

print("====== Non-image files ======")
for f in non_image_files:
    print(f)

print("\n====== Broken image files ======")
for f in broken_files:
    print(f)
