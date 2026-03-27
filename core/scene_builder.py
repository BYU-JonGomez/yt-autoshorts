from PIL import Image, ImageDraw
import config
from core.text_styles import get_fonts

fonts = get_fonts()

def draw_center(draw, text, font, color):
    bbox = draw.textbbox((0,0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.text(((config.WIDTH-w)//2, (config.HEIGHT-h)//2),
              text,
              fill=color,
              font=font)


def create_scene_pro(text_lines, filename, style="normal"):
    img = Image.new("RGB", (config.WIDTH, config.HEIGHT), config.BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    if style == "error":
        draw_center(draw, text_lines[0], fonts["big"], config.COLORS["red"])

    elif style == "fix":
        draw_center(draw, text_lines[0], fonts["big"], config.COLORS["green"])

    elif style == "dialog":
        draw.text((100, config.HEIGHT//2 - 120),
                  text_lines[0],
                  fill=config.COLORS["white"],
                  font=fonts["small"])

        w = draw.textbbox((0,0), text_lines[1], font=fonts["small"])[2]

        draw.text((config.WIDTH - w - 100, config.HEIGHT//2 + 20),
                  text_lines[1],
                  fill=config.COLORS["green"],
                  font=fonts["small"])

    else:
        draw_center(draw, "\n".join(text_lines), fonts["medium"], config.COLORS["white"])

    img.save(filename)