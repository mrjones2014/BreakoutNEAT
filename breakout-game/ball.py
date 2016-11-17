import pygame
import numpy
from game_params import *


class Ball(object):
    def __init__(self, x=0, y=0):
        self.image = pygame.image.load("../assets/ball.png")
        self.hitbox = self.image.get_rect()
        self.dx = 0
        self.dy = 0

    def move(self):
        if self.hitbox.left < 0 or self.hitbox.right > width:
            self.dx *= -1
        if self.hitbox.top < 0:
            self.dy *= -1
        self.hitbox.center = (self.hitbox.center[0] + self.dx, self.hitbox.center[1] + self.dy)

    def distance_to(self, x_other, y_other):
        return numpy.sqrt(numpy.power((self.hitbox.x - x_other), 2) + numpy.power((self.hitbox.y - y_other), 2))
