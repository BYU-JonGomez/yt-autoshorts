import subprocess
import config

def create_video(scene_files, durations, output):
    cmd = [config.FFMPEG_PATH, "-y"]

    for f, d in zip(scene_files, durations):
        cmd += ["-loop", "1", "-t", str(d), "-i", f]

    filter_complex = f"concat=n={len(scene_files)}:v=1:a=0,format=yuv420p[v]"

    cmd += ["-filter_complex", filter_complex, "-map", "[v]", output]

    subprocess.run(cmd)


def add_music(input_video, output_video):
    cmd = [
        config.FFMPEG_PATH, "-y",
        "-i", input_video,
        "-i", "assets/music.mp3",
        "-shortest",
        "-c:v", "copy",
        "-c:a", "aac",
        output_video
    ]

    subprocess.run(cmd)