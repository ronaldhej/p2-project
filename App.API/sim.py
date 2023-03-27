#import os
#os.environ["ARCADE_HEADLESS"] = "true"

import sys
from PIL import Image, ImageDraw
import arcade
import pymunk
import pyrender
import io
import math
import random
# import glcontext
# Create a 100 x 100 headless window

SPACE_WIDTH = 512
SPACE_HEIGHT = 512
FPS = 30
AGENT_RADIUS = 8
col_black = (0, 0, 0)

animation = []

class Agent:
    def __init__(self, pymunk_shape, color):
        self.center_x = pymunk_shape.body.position.x
        self.center_y = pymunk_shape.body.position.y
        self.radius = pymunk_shape.radius
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2
        self.angle = pymunk_shape.body.angle
        self.color = color
        self.pymunk_shape = pymunk_shape

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, self.color)

class Simulator(arcade.Window):
    #Initializing states for the game
    def __init__(self, agent_num):
        super().__init__(SPACE_WIDTH, SPACE_HEIGHT)
        self.space_width = SPACE_WIDTH
        self.space_height = SPACE_HEIGHT
        arcade.set_background_color((25,25,25))
        self.agent_num = agent_num
        self.space = pymunk.Space()
        self.space.iterations = 35
        self.space.gravity = (0.0, -900.0)
        self.person_list = []
        self.wall_list = []
        self.total_time = 0.0
        self.static_lines = []
        self.animation = []
        self.set_update_rate(1/FPS)

        #Add Map Boundaries
        #Lower
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, (0, 0), (SPACE_WIDTH, 0), 0.0)
        shape.friction = 10
        self.space.add(shape, body)
        self.static_lines.append(shape)
        #Upper
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, (0, SPACE_HEIGHT), (SPACE_WIDTH, SPACE_HEIGHT), 0.0)
        shape.friction = 10
        self.space.add(shape, body)
        self.static_lines.append(shape)
        #Left
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, (0, 0), (0, SPACE_HEIGHT), 0.0)
        shape.friction = 10
        self.space.add(shape, body)
        self.static_lines.append(shape)
        #Right
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, (SPACE_WIDTH, 0), (SPACE_WIDTH, SPACE_HEIGHT), 0.0)
        shape.friction = 10
        self.space.add(shape, body)
        self.static_lines.append(shape)
    
    def on_draw(self):
        self.clear()
        for person in self.person_list:
            person.draw()
        for wall in self.wall_list:
            wall.draw()
        for line in self.static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            arcade.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, (25,25,25), 5)

    def on_update(self, dt):
        if self.total_time >= 3:
            frame_image = arcade.get_image(0, 0, *self.get_size())
            self.animation.append(frame_image)
            print("Fuck")
            arcade.exit()
        else:
            #frame_image.save("framebuffer.png")
            
            self.total_time += dt
            self.space.step(1/FPS)
            for person in self.person_list:
                person.center_x = person.pymunk_shape.body.position.x
                person.center_y = person.pymunk_shape.body.position.y
                person.angle = math.degrees(person.pymunk_shape.body.angle)

            frame_image = arcade.get_image(0, 0, *self.get_size())
            self.animation.append(frame_image)
    
    def setup(self):
        for i in range(self.agent_num):
            inertia = pymunk.moment_for_circle(1, 0, AGENT_RADIUS, (0, 0))
            body = pymunk.Body(1,  inertia)
            body.position = (SPACE_WIDTH / 2) + (random.random()-0.5)*256, (SPACE_HEIGHT / 2) + (random.random()-0.5)*256
            shape = pymunk.Circle(body, AGENT_RADIUS, pymunk.Vec2d(0, 0))
            shape.friction = 0.3
            person = Agent(shape, (231, 191, 14))
            self.space.add(body, shape)
            self.person_list.append(person)

def run_agent_sim(frames, save, agent_num):
    window = Simulator(agent_num)
    window.setup()
    print("sim start")
    arcade.run()
    arcade.close_window()
    print("sim end")

    print("image count", len(window.animation))
    buffer = io.BytesIO()
    window.animation[0].save(buffer, format="GIF", save_all=True, append_images=window.animation[1:], optimize=True, duration=1000/30, loop=0)
    return buffer
        





def run_sim(coords, frames, save):
    """run simulation, return image"""
    window = arcade.open_window(SPACE_WIDTH, SPACE_HEIGHT)
    arcade.set_background_color((55, 55, 55))
    animation = []
    # window.headless = True

    # Draw a quick rectangle
    for frame in range(0, frames):
        print(f'current frame: {frame}\t size: {sys.getsizeof(animation)}')
        window.clear()
        arcade.draw_rectangle_filled(
            coords[0]+(frame/4), coords[1]+math.sin(frame/10)*100, 12, 12, (231, 191, 14))
        frame_image = arcade.get_image(0, 0, *window.get_size())
        animation.append(frame_image)
        if save:
            frame_image.save("framebuffer.png")

    buffer = io.BytesIO()
    animation[1].save(buffer, format="GIF",
                      save_all=True, append_images=animation[1:], optimize=True, duration=24, loop=0)

    window.close()
    return buffer
