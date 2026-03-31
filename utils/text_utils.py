from PIL import ImageFont

def auto_font_size(text, font_path, max_width, max_height, draw):
    size = 90

    while size > 20:
        font = ImageFont.truetype(font_path, size)
        lines = text.split("\n")

        total_height = 0
        for line in lines:
            bbox = draw.textbbox((0,0), line, font=font)
            total_height += (bbox[3] - bbox[1]) + 10

        if total_height <= max_height:
            return font, lines

        size -= 2

    return ImageFont.truetype(font_path, 20), lines