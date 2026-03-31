import subprocess
import config

def create_video(scene_files, durations, output_path):
    cmd = [config.FFMPEG_PATH, "-y"]

    for file, duration in zip(scene_files, durations):
        cmd += ["-loop", "1", "-t", str(duration), "-i", file]

    filters = []

    for i in range(len(scene_files)):
        filters.append(
            f"[{i}:v]zoompan=z='min(zoom+0.0015,1.08)':d=125:s=1080x1920,"
            f"fade=t=in:st=0:d=0.2,fade=t=out:st={durations[i]-0.2}:d=0.2[v{i}]"
        )

    concat = "".join([f"[v{i}]" for i in range(len(scene_files))])

    filter_complex = ";".join(filters) + f";{concat}concat=n={len(scene_files)}:v=1:a=0[v]"

    cmd += ["-filter_complex", filter_complex, "-map", "[v]", output_path]

    subprocess.run(cmd)