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
from flowfield import FlowField, Cell
import utility
from time import perf_counter
from colorsys import hsv_to_rgb
from fastapi import WebSocket
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
    def __init__(self, pymunk_shape, color, field_id):
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
        self.field_id = field_id


    def update_vel(self):
        '''update agent velocity'''
        self.pymunk_shape.body.velocity = (math.cos(self.direction)*self.magnitude,
                                           math.sin(self.direction)*self.magnitude)
        
    def draw(self):
        #Personal Space Circle
        risk = self.nearby_agents / 7
        color = utility.heatmap_rgb(risk)
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, (228, 79, 34))

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
        self.space.iterations = 100
        self.space.gravity = (0.0, 0.0)
        #Object Lists
        self.person_list: arcade.SpriteList[Agent] = arcade.SpriteList()

        #Data
        self.density_data:list[float] = []
        self.wall_list:list[pymunk.Poly] = []
        self.total_time = 0.0
        self.static_lines = []
        self.total_time = 0.0
        self.total_steps = 0
        self.animation = []
        self.field_list:list[FlowField] = []
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

    def add_wall(self, wall_verts: tuple[int,int]):
        '''add wall to wall list, with any number if integer points (more than 3)'''
        if len(wall_verts) < 3:
            return
        wall_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        wall_shape = pymunk.Poly(wall_body, wall_verts)
        wall_shape.friction = 10
        self.space.add(wall_shape, wall_body)
        self.wall_list.append(wall_shape)
    
    def on_draw(self):
        pass

    def on_update(self, dt):
        pass

    def setup(self):
        ...

    def add_agent(self, frame):
        if frame%2==0:    
            field_id = 0
            pos = (SPACE_WIDTH / 2) + (random.random()-0.5)*300, 32 + (random.random()-0.5)*16
        else:
            field_id = 1
            pos = (SPACE_WIDTH / 2) + (random.random()-0.5)*300, SPACE_HEIGHT - (random.random()-0.5)*16 - 32
        
        inertia = pymunk.moment_for_circle(1, 0, AGENT_RADIUS, (0, 0))
        body = pymunk.Body(1,  inertia)
        body.position = pos
        shape = pymunk.Circle(body, AGENT_RADIUS, pymunk.Vec2d(0, 0))
        shape.friction = 0.3
        person = Agent(shape, (231, 191, 14), field_id)
        person.direction = random.randrange(0,2) * math.pi
        self.space.add(body, shape)
        self.person_list.append(person)


class Scenario:
    def __init__(self, agent_num, runtime) -> None:
        pass


async def run_agent_sim(socket: WebSocket, frames, save, agent_num, runtime:int, resolution) -> tuple[io.BytesIO, list[int]]:
    """run simulation on input parameters and return results"""
    window = Simulator(agent_num, runtime, False)
    window.add_wall([
                    (4,128-32),
                    (256-16,128),
                    (256-14, SPACE_HEIGHT - 64),
                    (4,SPACE_HEIGHT - 32)])
    window.add_wall([
                    (SPACE_WIDTH - 4,128-32),
                    (256+16,128),
                    (256+14, SPACE_HEIGHT - 64),
                    (SPACE_WIDTH - 4,SPACE_HEIGHT - 32)])
    window.add_wall([
                    (256-32,72+8),
                    (256-32,72-8),
                    (256+32,72+40),
                    (256+140,72+16),
                    (256+128,72-8)])
    window.setup()
    
    print("sim start")
    agent_num_list = []
    # arcade.run()
    flowfield = FlowField(SPACE_WIDTH, SPACE_HEIGHT, resolution, (6,30))
    flowfield.setup(window.wall_list)
    window.field_list.append(flowfield)
    flowfield = FlowField(SPACE_WIDTH, SPACE_HEIGHT, resolution, (3,1))
    flowfield.setup(window.wall_list)
    window.field_list.append(flowfield)

    f_end = runtime*FPS
    t_add = 1
    for f in range(runtime*FPS):
        t_add -= 1
        if t_add <= 0:
            window.add_agent(f)
            window.add_agent(f+1)
            t_add = 1
        t_draw_start = perf_counter()
        sim_draw(window)
        t_draw_stop = perf_counter()
        t_update_start = perf_counter()
        sim_update(window)
        agent_num_list.append(len(window.person_list))
        t_update_stop = perf_counter()
        print(f'EXECUTION TIME [\tdraw: {(t_draw_stop - t_draw_start) * 1000:.2f}ms\t| update: {(t_update_stop - t_update_start) * 1000:.2f}ms \t] frame: {f+1}/{f_end}')
        await socket.send_json({"type":1,"agent_num_datapoint": len(window.person_list)})
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
    return buffer, agent_num_list

def draw_grid(res: int):
    for i in range(res):
        arcade.draw_line(SPACE_WIDTH/res*i,0,SPACE_WIDTH/res*i,SPACE_HEIGHT, (55,55,55), 1)
        arcade.draw_line(0,SPACE_HEIGHT/res*i,SPACE_WIDTH,SPACE_HEIGHT/res*i, (55,55,55), 1)

def sim_draw(sim: Simulator):
    """draw step of simulation"""
    sim.clear()
    #draw_grid(sim.flowfield.resolution)
    #sim.field_list[1].draw()

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
    #update flow field every second
    field_age += 1
    if field_age > FPS:
        for field in sim.field_list:
            field.update()
        field_age = 0
    for person in sim.person_list:
        
        xpos = person.pymunk_shape.body.position.x
        ypos = person.pymunk_shape.body.position.y
        person.center_x = xpos
        person.center_y = ypos
        dead = False
        #person.angle = math.degrees(person.pymunk_shape.body.angle)
        if xpos > 0 and xpos < SPACE_WIDTH and ypos > 0 and ypos < SPACE_HEIGHT:
            field = sim.field_list[person.field_id]
            cell:Cell = field.get_cell(xpos, ypos)
            person.target_direction = cell.direction
            if cell.cost < 4:
                dead = True
                sim.space.remove(person.pymunk_shape, person.pymunk_shape.body)
                sim.person_list.remove(person)
        else:
            pass #TODO set direction to center of space

        if dead:
            continue
        #person_near_list = arcade.check_for_collision_with_list(person, sim.person_list)        
        person.nearby_agents = 0#len(person_near_list)
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
    #density_data = DensityData(sim.total_steps, max(step_density_vals))
    #sim.density_data.append(density_data)
