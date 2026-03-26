import subprocess
import config

def check_ffmpeg():
    try:
        subprocess.run([config.FFMPEG_PATH, "-version"],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        print("FFmpeg OK")
    except:
        print("FFmpeg not found")
        exit()