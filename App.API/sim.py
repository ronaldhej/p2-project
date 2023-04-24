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
import matplotlib.pyplot as plt
from flowfield import FlowField
import utility
from time import perf_counter
from colorsys import hsv_to_rgb
# import glcontext

SPACE_WIDTH = 512
SPACE_HEIGHT = 512
FPS = 30

AGENT_RADIUS = 2
PERSONAL_SPACE = 3
col_black = (0, 0, 0)

animation = []

class DensityData:
    def __init__(self, step, value):
        self.step = step
        self.value = value

class Agent(arcade.Sprite):
    def __init__(self, pymunk_shape, color):
        super().__init__(center_x = pymunk_shape.body.position.x, center_y = pymunk_shape.body.position.y)
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
        self.nearby_agents = 0


    def update_vel(self):
        '''update agent velocity'''
        self.pymunk_shape.body.velocity = (math.cos(self.direction)*self.magnitude,
                                           math.sin(self.direction)*self.magnitude)
        
    def draw(self):
        #Personal Space Circle
        risk = self.nearby_agents / 7
        color = utility.heatmap_rgb(risk)
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, color)

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
        #Object Lists
        self.person_list: arcade.SpriteList[Agent] = arcade.SpriteList()

        #Data
        self.density_data = []
        self.wall_list:list[pymunk.Poly] = []
        self.total_time = 0.0
        self.static_lines = []
        self.total_time = 0.0
        self.total_steps = 0
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

        wall_verts_list:list[list[tuple[float, float]]] = [
                [
                    (4,128-32),
                    (256-16,128),
                    (256-14, SPACE_HEIGHT - 64),
                    (4,SPACE_HEIGHT - 32)
                ],[
                    (SPACE_WIDTH - 4,128-32),
                    (256+16,128),
                    (256+14, SPACE_HEIGHT - 64),
                    (SPACE_WIDTH - 4,SPACE_HEIGHT - 32)
                ],[
                    (256-32,72+8),
                    (256-32,72-8),
                    (256+32,72+40),
                    (256+140,72+16),
                    (256+128,72-8)
                ]
            ]
        
        for vs in wall_verts_list:
            wall_body = pymunk.Body(body_type=pymunk.Body.STATIC)
            wall_shape = pymunk.Poly(wall_body, vs)
            wall_shape.friction = 10

            self.space.add(wall_shape, wall_body)
            self.wall_list.append(wall_shape)
    
    def on_draw(self):
        pass

    def on_update(self, dt):
        pass

    def setup(self):
        for i in range(self.agent_num):
            inertia = pymunk.moment_for_circle(1, 0, AGENT_RADIUS, (0, 0))
            body = pymunk.Body(1,  inertia)
            body.position = (SPACE_WIDTH / 2) + (random.random()-0.5)*300, 32 + (random.random()-0.5)*16
            shape = pymunk.Circle(body, AGENT_RADIUS, pymunk.Vec2d(0, 0))
            shape.friction = 0.3
            person = Agent(shape, (231, 191, 14))
            person.direction = random.randrange(0,2) * math.pi
            self.space.add(body, shape)
            self.person_list.append(person)


class Scenario:
    def __init__(self, agent_num, runtime) -> None:
        pass


def run_agent_sim(frames, save, agent_num, runtime, resolution) -> tuple[io.BytesIO, list[DensityData]]:
    """run simulation on input parameters and return results"""
    window = Simulator(agent_num, runtime, False)
    window.setup()
    print("sim start")
    # arcade.run()
    flowfield = FlowField(SPACE_WIDTH, SPACE_HEIGHT, resolution)
    flowfield.setup(window.wall_list)

    window.flowfield = flowfield

    f_end = runtime*FPS
    for f in range(runtime*FPS):
        t_draw_start = perf_counter()
        sim_draw(window)
        t_draw_stop = perf_counter()
        t_update_start = perf_counter()
        sim_update(window)
        t_update_stop = perf_counter()
        print(f'EXECUTION TIME [\tdraw: {(t_draw_stop - t_draw_start) * 1000:.2f}ms\t| update: {(t_update_stop - t_update_start) * 1000:.2f}ms \t] frame: {f+1}/{f_end}')
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
    return buffer, window.density_data

def draw_grid(res: int):
    for i in range(res):
        arcade.draw_line(SPACE_WIDTH/res*i,0,SPACE_WIDTH/res*i,SPACE_HEIGHT, (55,55,55), 1)
        arcade.draw_line(0,SPACE_HEIGHT/res*i,SPACE_WIDTH,SPACE_HEIGHT/res*i, (55,55,55), 1)

def sim_draw(sim: Simulator):
    """draw step of simulation"""
    sim.clear()
    #draw_grid(sim.flowfield.resolution)
    #sim.flowfield.draw()

    for person in sim.person_list:
        person.draw()
    for wall in sim.wall_list:
        vs = wall.get_vertices()
        for v in vs:
            x,y = v.rotated(wall.body.angle) + wall.body.position
            v = (int(x), int(y))
        arcade.draw_polygon_outline(vs, (255,255,255),1)
    for line in sim.static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        arcade.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, (25,25,25), 5)

def sim_update(sim: Simulator):
    """update step of simulation"""
    sim.space.step(1/FPS)
    sim.total_steps += 1
    step_density_vals = []
    field_age = 0
    for person in sim.person_list:

        #update flow field every second
        field_age += 1
        if field_age > FPS:
            sim.flowfield.update()
            field_age = 0
        
        xpos = person.pymunk_shape.body.position.x
        ypos = person.pymunk_shape.body.position.y
        person.center_x = xpos
        person.center_y = ypos
        #person.angle = math.degrees(person.pymunk_shape.body.angle)
        if xpos > 0 and xpos < SPACE_WIDTH and ypos > 0 and ypos < SPACE_HEIGHT:
            person.target_direction = sim.flowfield.get_cell(xpos, ypos).direction
        else:
            pass #TODO set direction to center of space

        person_near_list = arcade.check_for_collision_with_list(person, sim.person_list)        
        person.nearby_agents = len(person_near_list)
        step_density_vals.append(person.nearby_agents)
        person.center_x = xpos
        person.center_y = ypos
        person.angle = math.degrees(person.pymunk_shape.body.angle)

        diff = ( person.target_direction - person.direction + math.pi ) % (2*math.pi) - math.pi
        if diff < -math.pi:
            diff = diff + 360
        person.direction = person.direction + (diff)*0.1
        person.update_vel()


    frame_image = arcade.get_image(0, 0, *sim.get_size())
    sim.animation.append(frame_image)
    density_data = DensityData(sim.total_steps, max(step_density_vals))
    sim.density_data.append(density_data)
    
def graph() -> io.BytesIO:
    x1 = [1,2,3]
    y1 = [2,4,1]
    plt.plot(x1, y1)
  
    plt.xlabel('Time')
    plt.ylabel('Max density')
    plt.title('Max density over time')

    image_buffer = io.BytesIO()

    plt.savefig(image_buffer, format='png', bbox_inches='tight')

    return image_buffer
