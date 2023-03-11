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
        self.person_list = []
        self.wall_list = []
        self.selection_box = None
        self.paused = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.box_start = (None, None)
        self.box_end = (None, None)
        person = entity.Person(50, 50, 20, 10, 0, 0, 0, arcade.color.WHITE)

        self.person_list.append(person)

    #Called on each update for the sake of drawing entities, sprites etc
    def on_draw(self):
        self.clear()
        arcade.draw_text("Press space to pause/unpause entity movement, c to clear walls", 50, 50, arcade.color.WHITE, 12)        
        for person in self.person_list:
            person.draw()
        for wall in self.wall_list:
            wall.draw()
        if self.selection_box != None:
            self.selection_box.draw()

    #Tick Updates
    def on_update(self, dt):
        if self.paused == False:
            for person in self.person_list:
                person.follow_mouse(self.mouse_x, self.mouse_y)

    #Input Handling
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_key_press(self, key, modifiers):
        match key:
            case arcade.key.SPACE:
                self.paused = not self.paused
            case arcade.key.C:
                self.wall_list.clear()
            case _:
                return

    def on_mouse_press(self, x, y, button, key_modifiers):
        LOG.debug("Mouse pressed")
        self.box_start = (x, y)
        vals = get_rectangle_vals(x, y, x, y)
        selection = entity.SelectionBox(*vals, arcade.color.WHITE, 2)
        self.selection_box = selection

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        start_x, start_y = self.box_start
        if start_x != None and start_y != None:
            vals = get_rectangle_vals(start_x, start_y, x, y)
            selection = entity.SelectionBox(*vals, arcade.color.WHITE, 2)
            self.selection_box = selection

    def on_mouse_release(self, x, y, button, modifiers):
        LOG.debug("Mouse just released")
        self.selection_box = None
        self.box_end = (x, y)
        vals = get_rectangle_vals(*self.box_start, *self.box_end)
        wall = entity.Wall(*vals, arcade.color.WHITE)
        self.wall_list.append(wall)

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
