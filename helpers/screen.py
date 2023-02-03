from PIL import ImageGrab
from helpers import color

def extract_color(saturated):
    image = ImageGrab.grab()
    
    bbox = image.convert("RGB").getbbox()
    if bbox:
        image = image.crop(bbox)
    
    palette = image.quantize(colors=1).getpalette()
    dominant_color = [palette[i:i + 3] for i in range(0, 3, 3)][0]
    return color.get_saturated_color(dominant_color) if saturated else dominant_color