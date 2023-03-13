import math
import arcade
import pymunk

PERSON_SPEED = 150


class Person:
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

   def follow_mouse(self, mouse_x, mouse_y):
      start_x = self.center_x
      start_y = self.center_y

      dest_x = mouse_x
      dest_y = mouse_y

      x_diff = dest_x - start_x
      y_diff = dest_y - start_y
      angle = math.atan2(y_diff, x_diff)      

      return math.cos(angle) * PERSON_SPEED, math.sin(angle) * PERSON_SPEED

class Wall:
   def __init__(self, pymunk_shape, center_x, center_y, width, height, color):
      self.center_x = center_x
      self.center_y = center_y
      self.width = width
      self.height = height
      self.color = color
      self.pymunk_shape = pymunk_shape

   def set_vals(self, center_x, center_y, width, height):
      self.center_x = center_x
      self.center_y = center_y
      self.width = width
      self.height = height
 
   def draw(self):
      arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, arcade.color.WHITE, 0)

class SelectionBox:
   def __init__(self, center_x, center_y, width, height, color, outline):
      self.center_x = center_x
      self.center_y = center_y
      self.width = width
      self.height = height
      self.color = color
      self.outline = outline

   def draw(self):
      arcade.draw_rectangle_outline(self.center_x, self.center_y, self.width, self.height, self.color, self.outline, 0)
