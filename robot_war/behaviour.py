import pygame
import math as m
from robot_war.game_utils import *

class Condition:
    def __init__(self):
        self.object = None

    def set_object(self, object):
        self.object = object
    
    def apply(self):
        pass

class Always(Condition):
    def __init__(self):
        super().__init__()

    def apply(self):
        return True

class TooClose(Condition):
    def __init__(self, target, radius):
        super().__init__()
        self.target = target
        self.radius = radius

    def apply(self):
        x_diff = self.object.x - self.target.x
        y_diff = self.object.y - self.target.y
        dist = m.sqrt(x_diff**2 + y_diff**2)
        print(dist)
        
        return dist < self.radius

class Behaviour:
    def __init__(self):
        self.object = None
        self.settings = GameSettingsFactory().get_settings()
    
    def set_object(self, object):
        self.object = object
    
    def do(self):
        pass

class PointBodyTo(Behaviour):
    def __init__(self, target):
        super().__init__()
        self.target = target
    
    def do(self):
        X = self.object.x + self.object.width // 2
        Y = self.object.y + self.object.height // 2

        angle = GameMath.rotation_angle_to(X, Y, self.target.x, self.target.y)
        self.object.body_rotation = angle

class MoveForward(Behaviour):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed

    def do(self):
        radian_angle = m.pi*(self.object.body_rotation - 270)/180.0
        self.object.vx = self.speed*m.cos(radian_angle)
        self.object.vy = (-1)*self.speed*m.sin(radian_angle)
