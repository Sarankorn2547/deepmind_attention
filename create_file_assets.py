import os
import random
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# Configuration
BASE_DIR = "benchmark_assets"
os.makedirs(BASE_DIR, exist_ok=True)
FILE_TYPES = ["png", "jpg", "pdf", "csv"]
COUNTS = 20  # 10 consistent + 10 conflicting per type

colors = ["red", "blue", "green", "yellow", "black"]
shapes = ["circle", "square"]
metrics = ["Revenue", "Profit", "Cost"]

def generate_image(path, color, shape):
    img = Image.new("RGB", (200, 200), white := (255, 255, 255))
    draw = ImageDraw.Draw(img)
    if shape == "circle":
        draw.ellipse((50, 50, 150, 150), fill=color, outline="black")
    else:
        draw.rectangle((50, 50, 150, 150), fill=color, outline="black")
    img.save(path)

def generate_pdf(path, metric, value):
    img = Image.new("RGB", (420, 240), "white")
    draw = ImageDraw.Draw(img)
    try:
        font_bold = ImageFont.truetype("arial.ttf", 20)
        font_regular = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()

    draw.text((20, 20), f"OFFICIAL REPORT: {metric}", fill="black", font=font_bold)
    draw.text((20, 80), f"The recorded {metric} value is {value}.", fill="black", font=font_regular)
    img.save(path, "PDF", resolution=100)

def generate_csv(path, metric, value):
    df = pd.DataFrame({"Metric": [metric], "Value": [value]})
    df.to_csv(path, index=False)

# File generation loop
for ftype in FILE_TYPES:
    for i in range(COUNTS):
        file_id = f"{ftype}_{i:02d}"
        path = os.path.join(BASE_DIR, f"{file_id}.{ftype}")
        
        if ftype in ["png", "jpg"]:
            generate_image(path, random.choice(colors), random.choice(shapes))
        elif ftype == "pdf":
            generate_pdf(path, random.choice(metrics), random.randint(10, 99))
        elif ftype == "csv":
            generate_csv(path, random.choice(metrics), random.randint(10, 99))

print(f"Successfully generated assets in /{BASE_DIR}")