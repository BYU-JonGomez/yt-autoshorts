import json
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import config

# Crear carpetas base
os.makedirs("output", exist_ok=True)
os.makedirs("temp", exist_ok=True)

# =========================
# VERIFICAR FFMPEG
# =========================
def check_ffmpeg():
    try:
        subprocess.run([config.FFMPEG_PATH, "-version"],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        print("✅ FFmpeg OK")
    except:
        print("❌ FFmpeg no encontrado")
        exit()

# =========================
# CREAR ESCENA
# =========================
def create_scene(text, filename, color_name):
    img = Image.new("RGB", (config.WIDTH, config.HEIGHT), config.BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(config.FONT_PATH, 80)
    color = config.COLORS[color_name]

    lines = text.split("\n")
    y_text = config.HEIGHT // 3

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        x = (config.WIDTH - w) // 2
        draw.text((x, y_text), line, fill=color, font=font)

        y_text += h + 25

    img.save(filename)

# =========================
# CREAR VIDEO
# =========================
def create_video(scene_files, durations, output_path):
    cmd = [config.FFMPEG_PATH, "-y"]

    for file, duration in zip(scene_files, durations):
        cmd += ["-loop", "1", "-t", str(duration), "-i", file]

    filter_complex = f"concat=n={len(scene_files)}:v=1:a=0,format=yuv420p[v]"

    cmd += [
        "-filter_complex", filter_complex,
        "-map", "[v]",
        output_path
    ]

    subprocess.run(cmd)

# =========================
# AGREGAR MÚSICA
# =========================
def add_music(video_input, video_output):
    cmd = [
        config.FFMPEG_PATH, "-y",
        "-i", video_input,
        "-i", "assets/music.mp3",
        "-shortest",
        "-c:v", "copy",
        "-c:a", "aac",
        video_output
    ]

    subprocess.run(cmd)

# =========================
# GENERAR VIDEO
# =========================
def generate_video(video_data, index):
    level = video_data["level"]
    temp_dir = f"temp/video_{index}"
    os.makedirs(temp_dir, exist_ok=True)

    level_folder = f"output/{level}"
    os.makedirs(level_folder, exist_ok=True)

    scenes = [
        (f"Level {level}", "white", config.DURATIONS["level"]),
        (video_data["hook"], "white", config.DURATIONS["hook"]),
        ("❌ " + video_data["error"], "red", config.DURATIONS["error"]),
        ("✅ " + video_data["fix"], "green", config.DURATIONS["fix"]),
        ("💡 " + video_data["grammar_tip"], "white", config.DURATIONS["grammar"]),
        ("🎓 " + video_data["class_tip"], "white", config.DURATIONS["class"]),
        ("\n".join(video_data["examples"]), "white", config.DURATIONS["examples"]),
        ("\n".join(video_data["real_example"]), "white", config.DURATIONS["real"]),
        ("💾 " + video_data["cta"], "white", config.DURATIONS["cta"]),
    ]

    scene_files = []
    durations = []

    for i, (text, color, duration) in enumerate(scenes):
        file_path = f"{temp_dir}/scene_{i}.png"
        create_scene(text, file_path, color)
        scene_files.append(file_path)
        durations.append(duration)

    raw_video = f"{temp_dir}/raw.mp4"
    final_video = f"{level_folder}/video_{index}.mp4"

    create_video(scene_files, durations, raw_video)
    add_music(raw_video, final_video)

    print(f"✅ Video generado: {final_video}")

# =========================
# MAIN
# =========================
def main():
    check_ffmpeg()

    with open("videos.json", "r", encoding="utf-8") as f:
        videos = json.load(f)

    for i, video in enumerate(videos):
        generate_video(video, i)

if __name__ == "__main__":
    main()
