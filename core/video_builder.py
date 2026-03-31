import subprocess
import config

def create_video(scene_files, durations, output_path):
    inputs = []
    filter_complex = ""

    for i, (file, duration) in enumerate(zip(scene_files, durations)):
        inputs += ["-loop", "1", "-t", str(duration), "-i", file]

        filter_complex += (
            f"[{i}:v]"
            f"scale=1080:1920,"
            f"fade=t=in:st=0:d=0.3,"
            f"fade=t=out:st={duration-0.3}:d=0.3"
            f"[v{i}];"
        )

    concat_inputs = "".join([f"[v{i}]" for i in range(len(scene_files))])

    filter_complex += (
        f"{concat_inputs}concat=n={len(scene_files)}:v=1:a=0,format=yuv420p[v]"
    )

    cmd = [
        config.FFMPEG_PATH,
        "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        output_path
    ]

    subprocess.run(cmd)