from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove

INPUT = Path("assets/images/source-photo.jpg")
OUTPUT = Path("assets/images/source-prepped.png")

if not INPUT.exists():
    raise FileNotFoundError(f"Image not found: {INPUT}")

print("Removing background...")

with open(INPUT, "rb") as f:
    input_bytes = f.read()

output_bytes = remove(input_bytes)

rgba = Image.open(__import__("io").BytesIO(output_bytes)).convert("RGBA")

# White background
background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
background.alpha_composite(rgba)

img = np.array(background.convert("RGB"))

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# CLAHE contrast enhancement
clahe = cv2.createCLAHE(
    clipLimit=2.5,
    tileGridSize=(8, 8)
)

gray = clahe.apply(gray)

cv2.imwrite(str(OUTPUT), gray)

print(f"Saved -> {OUTPUT}")