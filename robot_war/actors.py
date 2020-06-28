import pygame
import random
from robot_war.game_utils import *

class GameObject:
    def __init__(self, x=0, y=0, color=(0, 0, 0), width=0, height=0):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

        self.body_rotation = 0

        self.settings = GameSettingsFactory().get_settings()
        self.behaviors = []
        self.conditions = []

        ObjectLoopFactory().get_looper().add(self)

    def add_behaviour(self, condition, behaviour):
        behaviour.set_object(self)
        condition.set_object(self)
        self.conditions.append(condition)
        self.behaviors.append(behaviour)

    def update(self):
        for idx, behaviour in enumerate(self.behaviors):
            condition = self.conditions[idx]
            if condition.apply():
                behaviour.do()
            else:
                behaviour.clear()

        self.vx = self.vx + self.ax*self.settings.dt
        self.vy = self.vy + self.ay*self.settings.dt
        
        self.x = self.x + self.vx*self.settings.dt
        self.y = self.y + self.vy*self.settings.dt


class Cursor(GameObject):
    def __init__(self):
        super().__init__()

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()

    def draw(self, screen):
        pass

class Bullet(GameObject):
    def __init__(self, shooter, radius=2, color=(0,0,255)):
        super().__init__(color=color)
        self.shooter = shooter
        self.x = self.shooter.x + (self.shooter.width // 2)
        self.y = self.shooter.y + (self.shooter.height // 2)
        self.body_rotation = self.shooter.body_rotation
        self.radius = radius

    def update(self):
        super().update()
        if (self.x > self.settings.window_width) or \
        (self.x < 0) or (self.y > self.settings.window_height) or \
        (self.y < 0):
            looper = ObjectLoopFactory().get_looper()
            looper.drop_object(self)
            del self

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Robot(GameObject):
    def __init__(self, x=200, y=200, color=(255, 255, 0), width=100, height=100, 
    bullet_color=(0,0,255), lifebar_width=50, lifebar_height=5, lifebar_x_offset=8, lifebar_y_offset=8):
        super().__init__(x, y, color, width, height)
        self.bullet_color = bullet_color
        self.life = 100
        self.lifebar_width = lifebar_width
        self.lifebar_height = lifebar_height
        self.lifebar_x_offset = lifebar_x_offset
        self.lifebar_y_offset = lifebar_y_offset
        self.surface = pygame.Surface((1.01*self.height, 1.01*self.width), pygame.SRCALPHA)
        self.initialize_body()
    
    def initialize_body(self):
        pygame.draw.line(self.surface, self.color, (0, self.height), (self.width // 2, 0))
        pygame.draw.line(self.surface, self.color, (self.width // 2, 0), (self.width, self.height))
        pygame.draw.line(self.surface, self.color, (self.width, self.height), (0, self.height))
        pygame.draw.circle(self.surface, self.color, (self.width // 2, self.height // 2), 2)
        
    def draw_body(self, screen):
        previous_center = self.surface.get_rect().center
        rotated_surface = pygame.transform.rotate(self.surface, self.body_rotation)
        new_rect = rotated_surface.get_rect(center = previous_center)
        screen.blit(rotated_surface, (self.x + new_rect.topleft[0], self.y + new_rect.topleft[1]))

    def draw_lifebar(self, screen):
        try:
            x = self.x - self.lifebar_x_offset
            y = self.y - self.lifebar_y_offset

            width = self.life*self.lifebar_width/100.0
            pygame.draw.rect(screen, (255, 0, 0), (x, y, width, self.lifebar_height), 0)
        except:
            pass

    def draw(self, screen):
        self.draw_body(screen)
        self.draw_lifebar(screen)

