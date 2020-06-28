import pygame
import math as m
from datetime import datetime
from robot_war.game_utils import *
from robot_war.actors import *

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

        return dist < self.radius

class Behaviour:
    def __init__(self):
        self.object = None
        self.settings = GameSettingsFactory().get_settings()
    
    def set_object(self, object):
        self.object = object
    
    def do(self):
        pass

    def clear(self):
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
        self.firt_rotation = None

    def do(self):
        radian_angle = m.pi*(self.object.body_rotation - 270)/180.0
        self.object.vx = self.speed*m.cos(radian_angle)
        self.object.vy = (-1)*self.speed*m.sin(radian_angle)

class MoveSideways(Behaviour):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.first_rotation = None

    def do(self):
        if self.first_rotation is None:
            self.first_rotation = m.pi*(self.object.body_rotation - 270)/180.0
        
        radian_angle = self.first_rotation + m.pi/2
        self.object.vx = self.speed*m.cos(radian_angle)
        self.object.vy = (-1)*self.speed*m.sin(radian_angle)

    def clear(self):
        self.first_rotation = None

class Shoot(Behaviour):
    def __init__(self, cycles_interval):
        super().__init__()
        self.wait_time = cycles_interval*GameSettingsFactory().get_settings().dt
        self.last_time_shoot = None

    def do(self):
        now_time = datetime.now()
        if (self.last_time_shoot is None) or (now_time - self.last_time_shoot).total_seconds() > self.wait_time:
            bullet = Bullet(self.object, color=self.object.bullet_color)
            bullet.add_behaviour(Always(), MoveForward(60))
            self.last_time_shoot = now_time