from PIL import Image, ImageDraw
import arcade
import pyrender
import io
import os
import math
os.environ["ARCADE_HEADLESS"] = "true"
# import glcontext

# Create a 100 x 100 headless window

SPACE_WIDTH = 512
SPACE_HEIGHT = 512
col_black = (0, 0, 0)


def run_sim(coords, frames, save):
    """run simulation, return image"""
    window = arcade.open_window(SPACE_WIDTH, SPACE_HEIGHT)
    arcade.set_background_color((55, 55, 55))
    animation = []
    # window.headless = True

    # Draw a quick rectangle
    for frame in range(0, frames):
        print(f'current frame: {frame}')
        window.clear()
        arcade.draw_rectangle_filled(
            coords[0]+(frame/2), coords[1]+math.sin(frame/10)*100, 12, 12, (231, 191, 14))
        frame_image = arcade.get_image(0, 0, *window.get_size())
        animation.append(frame_image)
        if save:
            frame_image.save("framebuffer.png")

    buffer = io.BytesIO()
    animation[0].save(buffer, format="GIF",
                      save_all=True, append_images=animation[1:], optimize=True, duration=30, loop=0)

    window.close()
    return buffer
