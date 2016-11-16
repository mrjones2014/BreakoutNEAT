import pygame
from paddle import paddle
from ball import ball
from brick import brick

class breakout(object):
    def __init__(self, width, height):
        self.paddle = paddle()
        self.paddle.hitbox.move((width / 2) - (self.paddle.hitbox.right / 2), height - 20)
        self.ball = ball()
        self.ball.hitbox.move(width / 2, height / 2)
        self.ball.dx = 6
        self.ball.dy = 6