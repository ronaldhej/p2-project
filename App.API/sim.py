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
        self.direction = 0
        self.target_direction = 0
        self.magnitude = 20

    def update_vel(self):
        self.pymunk_shape.body.velocity = (math.cos(self.direction)*self.magnitude,
                                           math.sin(self.direction)*self.magnitude)

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, self.color)
        # arcade.draw_line(self.center_x,
        #             self.center_y,
        #             self.center_x+math.cos(self.direction)*16,
        #             self.center_y+math.sin(self.direction)*16,
        #             (0,0,255),2)

class Cell:
    def __init__(self, x:int, y:int) -> None:
        self.direction = 0
        self.weight = 1
        self.cost = 0
        self.x:int = x
        self.y:int = y

class FlowField:
    def __init__(self, width: int, height: int, resolution: int) -> None:
        self.width = width
        self.height = height
        self.cell_width: int = 0
        self.cell_height: int = 0
        self.cell_x: int = 0
        self.cell_y: int = 0
        self.resolution = resolution
        self.field = None

    def setup(self):
        """initialize cell arrays"""
        self.cell_width = round(self.width/16)
        self.cell_height = round(self.width/16)
        self.field = [[None]*self.resolution for _ in range(self.resolution)]
        print(self.cell_width)
        for i in range(self.resolution):
            for j in range(self.resolution):
                new_cell:Cell = Cell(i,j)
                new_cell.direction = math.radians(random.random()*360)
                self.field[i][j] = new_cell

    def update(self):
        pass

    def get_cell(self, x, y) -> Cell:
        cell_x = int(x / self.cell_width)
        cell_y = int(y / self.cell_height)
        return self.field[cell_x][cell_y]

    def draw(self):
        for x in range(0, self.resolution):
            for y in range(0, self.resolution):
                cell:Cell = self.field[x][y]
                center_x = self.cell_width*cell.x + self.cell_width/2
                center_y = self.cell_height*cell.y + self.cell_height/2
                arcade.draw_line(center_x,
                                 center_y,
                                 center_x+math.cos(cell.direction)*8,
                                 center_y+math.sin(cell.direction)*8,
                                 (255,255,255),1)
            # arcade.draw_line(x*self.cell_width,SPACE_HEIGHT,x*self.cell_width,0, (55,55,55))

class Simulator(arcade.Window):
    #Initializing states for the game
    def __init__(self, agent_num, runtime, multithreaded:bool):
        super().__init__(SPACE_WIDTH, SPACE_HEIGHT)
        self.space_width = SPACE_WIDTH
        self.space_height = SPACE_HEIGHT
        arcade.set_background_color((25,25,25))
        #request args
        self.agent_num = agent_num
        self.runtime = runtime
        #space
        self.space = pymunk.Space()
        self.space.iterations = 35
        self.space.gravity = (0.0, 0.0)
        self.person_list = []
        self.wall_list = []
        self.total_time = 0.0
        self.static_lines = []
        self.animation = []
        self.flowfield:FlowField = None

        self.space.collision_slop = 0

        #enable multithreading on other platforms than windows
        if sys.platform != "Win32" and multithreaded:
            self.space.threaded = True
            self.space.threads = 4

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
        pass
        # self.clear()
        # for person in self.person_list:
        #     person.draw()
        # for wall in self.wall_list:
        #     wall.draw()
        # for line in self.static_lines:
        #     body = line.body
        #     pv1 = body.position + line.a.rotated(body.angle)
        #     pv2 = body.position + line.b.rotated(body.angle)
        #     arcade.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, (25,25,25), 5)

    def on_update(self, dt):
        pass
        # if self.total_time >= self.runtime:
        #     frame_image = arcade.get_image(0, 0, *self.get_size())
        #     self.animation.append(frame_image)
        #     arcade.exit()
        # else:
        #     #frame_image.save("framebuffer.png")
            
        #     self.total_time += dt
        #     self.space.step(1/FPS)
        #     for person in self.person_list:
        #         person.center_x = person.pymunk_shape.body.position.x
        #         person.center_y = person.pymunk_shape.body.position.y
        #         person.angle = math.degrees(person.pymunk_shape.body.angle)

        #     frame_image = arcade.get_image(0, 0, *self.get_size())
        #     self.animation.append(frame_image)

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


class Scenario:
    def __init__(self, agent_num, runtime) -> None:
        pass


def run_agent_sim(frames, save, agent_num, runtime, resolution) -> io.BytesIO:
    """run simulation on input parameters and return results"""
    window = Simulator(agent_num, runtime, False)
    window.setup()
    print("sim start")
    # arcade.run()
    flowfield = FlowField(SPACE_WIDTH, SPACE_HEIGHT, resolution)
    flowfield.setup()

    window.flowfield = flowfield

    for _ in range(runtime*FPS):
        sim_draw(window)
        sim_update(window)
    arcade.exit()
    arcade.close_window()
    print("sim end")

    print("image count", len(window.animation))
    buffer = io.BytesIO()
    window.animation[0].save(buffer,
                             format="GIF",
                             save_all=True,
                             append_images=window.animation[1:],
                             optimize=True,
                             duration=1000/30,
                             loop=0)
    return buffer

def draw_grid(res: int):
    for i in range(res):
        arcade.draw_line(SPACE_WIDTH/res*i,0,SPACE_WIDTH/res*i,SPACE_HEIGHT, (55,55,55), 1)
        arcade.draw_line(0,SPACE_HEIGHT/res*i,SPACE_WIDTH,SPACE_HEIGHT/res*i, (55,55,55), 1)

def sim_draw(sim: Simulator):
    """draw step of simulation"""
    sim.clear()
    #draw_grid(16)
    #sim.flowfield.draw()
    for person in sim.person_list:
        person.draw()
    for wall in sim.wall_list:
        wall.draw()
    for line in sim.static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        arcade.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, (25,25,25), 5)

def sim_update(sim: Simulator):
    """update step of simulation"""
    sim.space.step(1/FPS)
    for person in sim.person_list:
        xpos = person.pymunk_shape.body.position.x
        ypos = person.pymunk_shape.body.position.y
        person.center_x = xpos
        person.center_y = ypos
        #person.angle = math.degrees(person.pymunk_shape.body.angle)
        person.target_direction = sim.flowfield.get_cell(xpos, ypos).direction

        diff = ( person.target_direction - person.direction + math.pi ) % (2*math.pi) - math.pi
        if diff < -math.pi:
            diff = diff + 360

        person.direction = person.direction + (diff)*0.1
        person.update_vel()


    frame_image = arcade.get_image(0, 0, *sim.get_size())
    sim.animation.append(frame_image)
