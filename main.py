import os
from PIL import Image, ImageDraw
import config

from core.ai_generator import generate_script
from core.video_builder import create_video
from utils.text_utils import auto_font_size

# Crear carpetas necesarias
os.makedirs("temp", exist_ok=True)
os.makedirs("output", exist_ok=True)


# =========================
# CREAR ESCENA (IMAGEN)
# =========================
def create_scene(text, path):
    img = Image.new("RGB", (config.WIDTH, config.HEIGHT), config.BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    # Forzar saltos de línea para mejor lectura
    text = text.replace(". ", ".\n")

    # Ajuste automático de fuente
    font, lines = auto_font_size(
        text,
        config.FONT_PATH,
        int(config.WIDTH * 0.8),
        int(config.HEIGHT * 0.6),
        draw
    )

    # Calcular altura total del bloque de texto
    total_height = 0
    line_sizes = []

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        h = bbox[3] - bbox[1]
        total_height += h + 15
        line_sizes.append((line, h))

    # Centrado vertical
    y = (config.HEIGHT - total_height) // 2

    # Dibujar texto centrado
    for line, h in line_sizes:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]

        x = (config.WIDTH - w) // 2
        draw.text((x, y), line, fill=config.COLORS["primary"], font=font)

        y += h + 15

    img.save(path)


# =========================
# GENERAR VIDEO COMPLETO
# =========================
def build_video(data, index):
    level = data["level"]

    # Crear carpeta por nivel
    level_folder = f"output/{level}"
    os.makedirs(level_folder, exist_ok=True)

    # Escenas del video
    scenes = [
        data["hook"],
        "❌ " + data["error"],
        "✅ " + data["fix"],
        "💡 " + data["grammar_tip"],
        "🎓 " + data["class_tip"],
        "\n".join(data["examples"]),
        "\n".join(data["real_example"]),
        "💾 " + data["cta"]
    ]

    # Duraciones por escena (segundos)
    durations = [2, 2, 2, 2, 2, 2, 2, 1]

    scene_files = []

    # Crear imágenes
    for i, text in enumerate(scenes):
        path = f"temp/{index}_{i}.png"
        create_scene(text, path)
        scene_files.append(path)

    # Ruta final del video
    output_path = f"{level_folder}/video_{index}.mp4"

    # Crear video
    create_video(scene_files, durations, output_path)

    print(f"✅ Video generado: {output_path}")


# =========================
# MAIN
# =========================
def main():
    print("🚀 INICIANDO SISTEMA...\n")

    levels = ["A1", "A2", "B1", "B2", "C1"]

    # Generar 1 video de prueba
    level = "A1"

    data = generate_script(level)

    print("📄 DATA GENERADA:\n")
    print(data)
    print("\n🎬 GENERANDO VIDEO...\n")

    build_video(data, 0)


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()