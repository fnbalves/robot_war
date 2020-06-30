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
shooter1 = Robot(bullet_color=(0,0,255))
shooter2 = Robot(x=500, y=500, color=(255, 0, 0), bullet_color=(0, 255, 255))

shooter1.body_rotation = 90
shooter1.add_behaviour(CollidesWith(AnyBullet()), TakeDamage(10))
shooter1.add_behaviour(Always(), PointBodyTo(shooter2))
shooter1.add_behaviour(Always(), MoveForward(30))
shooter1.add_behaviour(TooClose(shooter2, 150), MoveSideways(50))
shooter1.add_behaviour(TooClose(shooter2, 150), Shoot(50))

shooter2.add_behaviour(Always(), PointBodyTo(shooter1))
shooter2.add_behaviour(CollidesWith(AnyBullet()), TakeDamage(10))
shooter2.add_behaviour(Always(), MoveForward(30))
shooter2.add_behaviour(TooClose(shooter1, 150), Shoot(50))
shooter2.add_behaviour(TooClose(AnyBullet(), 150), MoveSideways(50))

#Game loop
while settings.active:
    for event in pygame.event.get():
        pass
    settings.screen.fill(settings.background_color)
    
    updater.update()
    pygame.display.flip()
    clock.tick(settings.game_frequency)
