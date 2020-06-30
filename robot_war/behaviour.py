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

class AnyBullet:
    def __init__(self):
        pass
    
class TooClose(Condition):
    def __init__(self, target, radius):
        super().__init__()
        self.target = target
        self.radius = radius

    def apply(self):
        if isinstance(self.target, AnyBullet):
            looper = ObjectLoopFactory().get_looper()
            bullets = [o for o in looper.objects if isinstance(o, Bullet)]
            for b in bullets:
                dist = GameMath.dist(b, self.object)
                if dist < self.radius:
                    return True
            return False
        else:
            return GameMath.dist(self.object, self.target) < self.radius

class CollidesWith(Condition):
    def __init__(self, target):
        super().__init__()
        self.target = target
        self.still_collided = False

    @staticmethod
    def have_collision(object1, object2):
        if pygame.sprite.collide_rect(object1, object2):
            offset = (int(object2.mask_x - object1.mask_x), int(object2.mask_y - object1.mask_y))
            if object1.mask.overlap(object2.mask, offset) is not None:
                return True
        return False

    def apply(self):
        if isinstance(self.target, AnyBullet):
            looper = ObjectLoopFactory().get_looper()
            bullets = [o for o in looper.objects if isinstance(o, Bullet)]
            for b in bullets:
                has_c = CollidesWith.have_collision(self.object, b)
                if has_c and b.shooter != self.object:
                    looper.drop_object(b)
                    return True
            return False
        else:
            has_c = CollidesWith.have_collision(self.object, self.target)
            if has_c and not self.still_collided:
                self.still_collided = True
                return True
            elif not has_c:
                self.still_collided = False
            return False

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

class TakeDamage(Behaviour):
    def __init__(self, damage):
        super().__init__()
        self.damage = damage
    
    def do(self):
        if self.object.life > 0:
            self.object.life -= self.damage
        else:
            self.object.life = 0