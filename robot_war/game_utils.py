import pygame
import math as m

class GameSettings:
    window_height = 500
    window_width = 500
    game_frequency = 70
    dt = 1 / game_frequency
    background_color = (0, 0, 0)
    screen = pygame.display.set_mode((window_width, window_height))
    active = True

    def set_window_bounds(self, window_height, window_width):
        GameSettings.window_height = window_height
        GameSettings.window_width = window_width
        GameSettings.screen = pygame.display.set_mode((GameSettings.window_width, GameSettings.window_height))

    def set_game_frequency(self, game_frequency):
        GameSettings.game_frequency = game_frequency
        GameSettings.dt = 1/GameSettings.game_frequency

    def set_active(self, active):
        GameSettings.active = active

    def set_background_color(self, color):
        GameSettings.background_color = color

class GameSettingsFactory:
    settings = None

    def get_settings(self):
        if GameSettingsFactory.settings is None:
            GameSettingsFactory.settings = GameSettings()
        return GameSettingsFactory.settings

class ObjectLooper:
    def __init__(self):
        self.objects = []
        self.settings = GameSettingsFactory().get_settings()

    def add(self, obj):
        self.objects.append(obj)
    
    def update(self):
        for obj in self.objects:
            obj.update()
            obj.draw(self.settings.screen)

    def drop_object(self, object):
        matching_indexes = [idx for idx, o in enumerate(self.objects) if o == object]
        for idx in matching_indexes:
            del self.objects[idx]

class ObjectLoopFactory:
    looper = None
    def __init__(self):
        pass

    def get_looper(self):
        if ObjectLoopFactory.looper is None:
            ObjectLoopFactory.looper = ObjectLooper()
        return ObjectLoopFactory.looper

class GameMath:
    @staticmethod
    def raw_angle(x1, y1, x2, y2):
        x_diff = x2 - x1
        y_diff = y2 - y1

        dist = m.sqrt(x_diff**2 + y_diff**2)
        return m.acos(x_diff/dist)
        
    @staticmethod
    def rotation_angle_to(x1, y1, x2, y2):
        
        try:
            rad_angle = GameMath.raw_angle(x1, y1, x2, y2)
            grad_angle = 180*rad_angle/m.pi

            if y2 < y1:
                grad_angle = 270 + grad_angle
            else:
                grad_angle = 360 - (grad_angle + 90)

            return grad_angle
        except:
            return 0