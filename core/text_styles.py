from PIL import ImageFont
import config

def get_fonts():
    return {
        "big": ImageFont.truetype(config.FONT_BOLD, 110),
        "medium": ImageFont.truetype(config.FONT_BOLD, 80),
        "small": ImageFont.truetype(config.FONT_REGULAR, 60)
    }