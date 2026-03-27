import os
from core.ai_generator import generate_multiple
from core.scene_builder import create_scene_pro
from core.video_builder import create_video, add_music
from core.utils import check_ffmpeg, validate_script
import config

os.makedirs("output", exist_ok=True)
os.makedirs("temp", exist_ok=True)


def generate_video(data, index):
    if not validate_script(data):
        print("Invalid script skipped")
        return

    level = data["level"]

    temp_dir = f"temp/video_{index}"
    os.makedirs(temp_dir, exist_ok=True)

    level_dir = f"output/{level}"
    os.makedirs(level_dir, exist_ok=True)

    scenes = [
        ([f"Level {level}"], "normal", config.DURATIONS["level"]),
        ([data["hook"]], "normal", config.DURATIONS["hook"]),
        (["❌ " + data["error"]], "error", config.DURATIONS["error"]),
        (["✅ " + data["fix"]], "fix", config.DURATIONS["fix"]),
        ([data["grammar_tip"]], "normal", config.DURATIONS["grammar"]),
        ([data["class_tip"]], "normal", config.DURATIONS["class"]),
        (data["examples"], "normal", config.DURATIONS["examples"]),
        (data["real_example"], "dialog", config.DURATIONS["real"]),
        ([data["cta"]], "normal", config.DURATIONS["cta"])
    ]

    files = []
    durations = []

    for i, (text, style, duration) in enumerate(scenes):
        file = f"{temp_dir}/scene_{i}.png"
        create_scene_pro(text, file, style)
        files.append(file)
        durations.append(duration)

    raw = f"{temp_dir}/raw.mp4"
    final = f"{level_dir}/video_{index}.mp4"

    create_video(files, durations, raw)
    add_music(raw, final)

    print(f"Video creado: {final}")


def main():
    check_ffmpeg()

    levels = ["A1", "A2", "B1", "B2", "C1"]

    scripts = generate_multiple(levels, 1)

    for i, script in enumerate(scripts):
        generate_video(script, i)


if __name__ == "__main__":
    main()