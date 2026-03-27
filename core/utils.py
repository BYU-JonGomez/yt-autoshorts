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


def validate_script(script):
    required = [
        "hook", "error", "fix",
        "grammar_tip", "class_tip",
        "examples", "real_example"
    ]

    return all(k in script for k in required)