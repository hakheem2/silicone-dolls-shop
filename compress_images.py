from PIL import Image
import os

def compress_images(directory, quality=70):
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                filepath = os.path.join(foldername, filename)
                try:
                    img = Image.open(filepath)

                    # Convert to RGB if image is .png or has transparency
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")

                    img.save(filepath, optimize=True, quality=quality)
                    print(f"✅ Compressed: {filepath}")
                except Exception as e:
                    print(f"❌ Failed to compress {filepath}: {e}")

# 🔁 Replace with your actual static images path
compress_images('static/images', quality=50)
