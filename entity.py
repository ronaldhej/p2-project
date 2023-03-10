import math
import arcade
import pymunk

PERSON_SPEED = 2

class Person:
   def __init__(self, center_x, center_y, radius, angle, delta_x, delta_y, delta_angle, color):
      self.center_x = center_x
      self.center_y = center_y
      self.radius = radius
      self.angle = angle
      self.delta_x = delta_x
      self.delta_y = delta_y
      self.delta_angle = delta_angle
      self.color = color
      
   def draw(self):
      arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, self.color, self.angle)

   def follow_mouse(self, mouse_x, mouse_y):
      self.center_x += self.delta_x
      self.center_y += self.delta_y

      start_x = self.center_x
      start_y = self.center_y

      dest_x = mouse_x
      dest_y = mouse_y

      x_diff = dest_x - start_x
      y_diff = dest_y - start_y
      angle = math.atan2(y_diff, x_diff)      

      self.delta_x = math.cos(angle) * PERSON_SPEED
      self.delta_y = math.sin(angle) * PERSON_SPEED

