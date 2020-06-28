import pygame
from robot_war.game_utils import *

class Cursor:
    def __init__(self):
        self.x = 0
        self.y = 0
        ObjectLoopFactory().get_looper().add(self)

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()

    def draw(self, screen):
        pass


class Robot:
    def __init__(self, x=200, y=200, color=(255, 255, 0), width=100, height=100):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

        self.settings = GameSettingsFactory().get_settings()

        self.height = height
        self.width = width
        self.color = color
        self.shooter_size = self.width // 3
        self.body_rotation = 0
        self.shooter_rotation = 0
        self.surface = pygame.Surface((1.01*self.height, 1.01*self.width), pygame.SRCALPHA)
        self.initialize_body()
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

        self.vx = self.vx + self.ax*self.settings.dt
        self.vy = self.vy + self.ay*self.settings.dt
        
        self.x = self.x + self.vx*self.settings.dt
        self.y = self.y + self.vy*self.settings.dt

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

    def draw(self, screen):
        self.draw_body(screen)

