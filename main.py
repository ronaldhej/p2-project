import arcade
import pymunk
import entity

#Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Crowd Crush Simulator"

class Simulator(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        
        self.person_list = []
        self.mouse_x = 0
        self.mouse_y = 0
        person = entity.Person(50, 50, 20, 10, 0, 0, 0, arcade.color.WHITE)

        self.person_list.append(person)

    def on_draw(self):
        self.clear()
        for person in self.person_list:
            person.draw()

    def on_update(self, dt):
        for person in self.person_list:
            person.follow_mouse(self.mouse_x, self.mouse_y)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

def main():
    window = Simulator()
    arcade.run()

if __name__ == "__main__":
    main()
