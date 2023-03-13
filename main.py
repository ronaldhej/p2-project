import math
import logging
import arcade
import pymunk
import entity

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger('arcade')
#Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Crowd Crush Simulator"

class Simulator(arcade.Window):
    #Initializing states for the game
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.space = pymunk.Space()
        self.space.iterations = 35
        self.space.gravity = (0.0, 0.0)
        self.space.damping = 0.1
        self.person_list = []
        self.wall_list = []
        self.static_lines = []
        self.selection_box = None
        self.paused = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.box_start = (None, None)
        self.box_end = (None, None)

        #Add Map Boundaries
        #Lower
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, (0, 0), (SCREEN_WIDTH, 0), 0.0)
        shape.friction = 10
        self.space.add(shape, body)
        self.static_lines.append(shape)
        #Upper
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), 0.0)
        shape.friction = 10
        self.space.add(shape, body)
        self.static_lines.append(shape)
        #Left
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, (0, 0), (0, SCREEN_HEIGHT), 0.0)
        shape.friction = 10
        self.space.add(shape, body)
        self.static_lines.append(shape)
        #Right
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), 0.0)
        shape.friction = 10
        self.space.add(shape, body)
        self.static_lines.append(shape)
        

    #Called on each update for the sake of drawing entities, sprites etc
    def on_draw(self):
        self.clear()
        arcade.draw_text("Press space to pause/unpause entity movement. Mouse left: wall, Mouse Right: Spawn Person", 50, 50, arcade.color.WHITE, 12)        
        for person in self.person_list:
            person.draw()
        for wall in self.wall_list:
            wall.draw()
        #Draw Map Boundaries
        for line in self.static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            arcade.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, arcade.color.WHITE, 5)
        if self.selection_box != None:
            self.selection_box.draw()

    #Tick Updates
    def on_update(self, dt):
        if self.paused:
            return
        else:
            self.space.step(1/60)
            for person in self.person_list:
                #Add force to follow mouse
                person.pymunk_shape.body.apply_force_at_local_point(person.follow_mouse(self.mouse_x, self.mouse_y))
                #Update draw position to physics object position
                person.center_x = person.pymunk_shape.body.position.x
                person.center_y = person.pymunk_shape.body.position.y
                person.angle = math.degrees(person.pymunk_shape.body.angle)

    #Input Handling
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_key_press(self, key, modifiers):
        match key:
            case arcade.key.SPACE:
                self.paused = not self.paused
            case arcade.key.C:
                for wall in self.wall_list:
                    self.space.remove(wall.pymunk_shape, wall.pymunk_shape.body)                    
                self.wall_list.clear()
            case _:
                return

    def on_mouse_press(self, x, y, button, key_modifiers):
        LOG.debug("Mouse pressed: %s", button)
        #If left click, begin drawing selection box
        if button == 1:
            self.box_start = (x, y)
            vals = get_rectangle_vals(x, y, x, y)
            selection = entity.SelectionBox(*vals, arcade.color.WHITE, 2)
            self.selection_box = selection
        #If right click, add person
        else:
            inertia = pymunk.moment_for_circle(1, 0, 20, (0, 0))
            body = pymunk.Body(1,  inertia)
            body.position = x, y
            shape = pymunk.Circle(body, 20, pymunk.Vec2d(0, 0))
            shape.friction = 0.3
            person = entity.Person(shape, arcade.color.WHITE)
            self.space.add(body, shape)
            self.person_list.append(person)

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        #If left click dragging, draw selection box
        if buttons == 1:
            start_x, start_y = self.box_start
            if start_x != None and start_y != None:
                vals = get_rectangle_vals(start_x, start_y, x, y)
                selection = entity.SelectionBox(*vals, arcade.color.WHITE, 2)
                self.selection_box = selection
        else:
            return

    def on_mouse_release(self, x, y, button, modifiers):
        #If left click is released, draw final box
        if button == 1:
            LOG.debug("Mouse just released")
            self.selection_box = None
            self.box_end = (x, y)
            center_x, center_y, width, height = get_rectangle_vals(*self.box_start, *self.box_end)
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pymunk.Vec2d(center_x, center_y)
            shape = pymunk.Poly.create_box(body, (width, height))
            wall = entity.Wall(shape, center_x, center_y, width, height, arcade.color.WHITE)
            self.space.add(body, shape)
            self.wall_list.append(wall)
        else:
            return

#Utility Functions
def get_rectangle_vals(start_x, start_y, end_x, end_y):
    center_x = (start_x/2) + (end_x/2)
    center_y = (start_y/2) + (end_y/2)
    width = end_x - start_x
    height = end_y - start_y
    return center_x, center_y, width, height

#Main Functions
def main():
    window = Simulator()
    arcade.run()

if __name__ == "__main__":
    main()
