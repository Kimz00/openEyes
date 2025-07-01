# text_utils.py
# 한글변환
from PIL import ImageFont, ImageDraw, Image
import numpy as np

def draw_text_korean(image, text, position, font_path='malgun.ttf', font_size=32, color=(255, 0, 0)):
    img_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill=color)
    return np.array(img_pil)
