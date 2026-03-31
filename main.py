import os
from PIL import Image, ImageDraw
import config

from core.ai_generator import generate_script
from core.video_builder import create_video
from utils.text_utils import auto_font_size

os.makedirs("temp", exist_ok=True)

def create_scene(text, path):
    img = Image.new("RGB", (config.WIDTH, config.HEIGHT), config.BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    # forzar saltos de línea naturales
    text = text.replace(". ", ".\n")

    font, lines = auto_font_size(
        text,
        config.FONT_PATH,
        config.WIDTH * 0.8,
        config.HEIGHT * 0.6,
        draw
    )

    total_height = 0
    line_sizes = []

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        h = bbox[3] - bbox[1]
        total_height += h + 15
        line_sizes.append((line, h))

    y = (config.HEIGHT - total_height) // 2

    for line, h in line_sizes:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]

        x = (config.WIDTH - w) // 2
        draw.text((x, y), line, fill=(255,255,255), font=font)

        y += h + 15

    img.save(path)

def build_video(data, index):
    scenes = [
        data["hook"],
        "❌ " + data["error"],
        "✅ " + data["fix"],
        data["grammar_tip"],
        data["class_tip"],
        "\n".join(data["real_example"]),
        data["cta"]
    ]

    files = []
    durations = [2,2,2,2,2,2,1]

    for i, text in enumerate(scenes):
        path = f"temp/{index}_{i}.png"
        create_scene(text, path)
        files.append(path)

    output = f"output/{data['level']}/video_{index}.mp4"
    os.makedirs(f"output/{data['level']}", exist_ok=True)

    create_video(files, durations, output)

# def main():
#     levels = ["A1","A2","B1","B2","C1"]

#     for i in range(3):
#         level = levels[i]
#         data = generate_script(level)
#         build_video(data, i)


    
def main():
    level = "A1"

    data = generate_script(level)

    print("\n📄 DATA GENERADA:\n")
    print(data)

    build_video(data, 0)

