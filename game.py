import pygame
import time
from robot_war.game_utils import *
from robot_war.actors import *
from robot_war.behaviour import *

settings = GameSettingsFactory().get_settings()
settings.set_game_frequency(30)
settings.set_window_bounds(1000, 1000)

pygame.init()
clock = pygame.time.Clock()

updater = ObjectLoopFactory().get_looper()

cursor = Cursor()
shooter1 = Robot()
shooter2 = Robot(x=500, y=500, color=(255, 0, 0))

shooter1.add_behaviour(Always(), PointBodyTo(shooter2))
shooter1.add_behaviour(Always(), MoveForward(30))
shooter1.add_behaviour(TooClose(shooter2, 150), MoveSideways(50))

shooter2.add_behaviour(Always(), PointBodyTo(shooter1))
shooter2.add_behaviour(Always(), MoveForward(30))

#Game loop
while settings.active:
    for event in pygame.event.get():
        pass
    settings.screen.fill(settings.background_color)

    updater.update()
    pygame.display.flip()
    clock.tick(settings.game_frequency)