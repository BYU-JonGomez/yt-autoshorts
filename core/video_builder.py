import subprocess
import config


def create_video(scene_files, durations, output_path):
    """
    Crea un video a partir de imágenes (escenas) usando FFmpeg.
    Cada imagen se muestra durante el tiempo definido en durations.
    """

    cmd = [config.FFMPEG_PATH, "-y"]

    # =========================
    # INPUTS (IMÁGENES)
    # =========================
    for file, duration in zip(scene_files, durations):
        cmd += [
            "-loop", "1",
            "-t", str(duration),
            "-i", file
        ]

    # =========================
    # FILTROS POR ESCENA
    # =========================
    filters = []

    for i, duration in enumerate(durations):
        filters.append(
            f"[{i}:v]"
            f"scale=1080:1920,"
            f"fps=30,"
            f"fade=t=in:st=0:d=0.3,"
            f"fade=t=out:st={max(duration - 0.3, 0.1)}:d=0.3"
            f"[v{i}]"
        )

    # =========================
    # CONCATENACIÓN
    # =========================
    concat_inputs = "".join([f"[v{i}]" for i in range(len(scene_files))])

    filter_complex = (
        ";".join(filters) +
        f";{concat_inputs}concat=n={len(scene_files)}:v=1:a=0,format=yuv420p[v]"
    )

    # =========================
    # COMANDO FINAL
    # =========================
    cmd += [
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-movflags", "+faststart",
        output_path
    ]

    # =========================
    # EJECUCIÓN
    # =========================
    try:
        print("\n🎬 Generando video...\n")
        subprocess.run(cmd, check=True)
        print(f"✅ Video creado: {output_path}")

    except subprocess.CalledProcessError as e:
        print("❌ Error en FFmpeg:")
        print(e)