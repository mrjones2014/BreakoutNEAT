import pygame
from breakout import Breakout
from game_params import *
import sys

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.key.set_repeat(1, 30)
game = Breakout(screen)
while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_q:
                sys.exit()
            if event.key == pygame.K_LEFT:
                game.paddle.move_left()
            if event.key == pygame.K_RIGHT:
                game.paddle.move_right()
            if event.key == pygame.K_r:
                game.reset()
    game.update()
    pygame.display.flip()

