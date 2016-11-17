import pygame
from game_params import *


class Paddle(object):
    def __init__(self):
        self.image = pygame.image.load("../assets/bat.png")
        self.hitbox = self.image.get_rect()
        self.hitbox = self.hitbox.move(self.hitbox.left, height - self.hitbox.bottom)

    def move_left(self):
        if self.hitbox.left > 0:
            self.hitbox.center = (self.hitbox.center[0] - paddle_speed, self.hitbox.center[1])
        if self.hitbox.left < 0:
            self.hitbox.center = (0, self.hitbox.center[1])

    def move_right(self):
        if self.hitbox.right < width:
            self.hitbox.center = (self.hitbox.center[0] + paddle_speed, self.hitbox.center[1])
        while self.hitbox.right > width:
            self.hitbox.center = (self.hitbox.center[0] - 1, self.hitbox.center[1])

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
            return True
        else:
            return False

    def get_center(self):
        return self.hitbox.center
