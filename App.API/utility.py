from colorsys import hsv_to_rgb
from arcade import Color

def heatmap_rgb(frac: float) -> Color:
    '''
    convert a floating point value (0-1) to a color with a hue between blue and red
    
    0: blue

    1: red
    '''
    hue_range = 240/360#blue-red range of hue
    hue = (1-min(frac, 1)) * hue_range
    color_float = hsv_to_rgb(hue,1,1)
    red,green,blue = color_float
    color:Color = (red*255, green*255, blue*255)
    return color
