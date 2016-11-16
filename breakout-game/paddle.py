import pygame
import numpy
from game_params import *


class paddle(object):
    def __init__(self):
        self.image = pygame.image.load("assets/bat.png")
        self.hitbox = self.image.get_rect()

    def move_left(self):
        self.hitbox.move(self.hitbox.x - paddle_speed, self.hitbox.y)

    def move_right(self):
        self.hitbox.move(self.hitbox.x + paddle_speed, self.hitbox.y)

    def reflect_ball_if_hit(self, ball):
        if self.hitbox.top <= ball.hitbox.bottom <= self.hitbox.bottom and ball.hitbox.right >= self.hitbox.left and \
                        ball.hitbox.left <= self.hitbox.right:
            ball.dy *= -1
            offset = ball.hitbox.center[0] - self.hitbox.center[0]
            if offset > 0:
                if offset > 30:
                    ball.dx = 7
                elif offset > 23:
                    ball.dx = 6
                elif offset > 17:
                    ball.dx = 5
            else:
                if offset < -30:
                    ball.dx = -7
                elif offset < -23:
                    ball.dx = -6
                elif ball.dx < -17:
                    ball.dx = -5
