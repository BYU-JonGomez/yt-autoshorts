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

    font, lines = auto_font_size(
        text,
        config.FONT_PATH,
        config.WIDTH * 0.8,
        config.HEIGHT * 0.6,
        draw
    )

    y = config.HEIGHT // 3

    for line in lines:
        draw.text((100, y), line, fill=(255,255,255), font=font)
        y += 80

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

if __name__ == "__main__":
    main()