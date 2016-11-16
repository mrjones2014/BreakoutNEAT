import pygame
import numpy


class ball(object):
    def __init__(self, x=0, y=0):
        self.image = pygame.image.load("assets/ball.png")
        self.hitbox = self.image.get_rect()
        self.dx = 0
        self.dy = 0

    def move(self):
        self.hitbox.move(self.hitbox.x + self.dx, self.hitbox.y + self.dy)

    def distance_to(self, x_other, y_other):
        return numpy.sqrt(numpy.power((self.hitbox.x - x_other), 2) + numpy.power((self.hitbox.y - y_other), 2))
