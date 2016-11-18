import pygame
from paddle import Paddle
from ball import Ball
from wall import Wall
from game_params import *
import random


class Breakout(object):
    def __init__(self, screen):
        self.num_times_hit_paddle = 0
        self.game_over = False
        self.time = 0
        self.paddle = Paddle()
        self.paddle.hitbox.move((width / 2) - (self.paddle.hitbox.right / 2), height - 20)
        self.ball = Ball()
        self.ball.hitbox.center = (width / 2, height / 2)
        self.init_ball_xspeed = 6
        self.init_ball_yspeed = 6
        self.ball.dx = self.init_ball_xspeed
        self.ball.dy = self.init_ball_yspeed
        self.wall = Wall()
        self.score = 0
        self.lives = init_lives
        self.screen = screen
        self.game_over_msg = pygame.font.Font(None, 70).render("Game Over", True, (0, 255, 255), bgcolor)

    def update(self):
        if not self.game_over:
            self.time += 1
        if self.ball.hitbox.top > height and self.lives > 0:
            self.lives -= 1
            self.ball.dx = self.init_ball_xspeed
            if random.random() > 0.5:
                self.ball.dx *= -1
            self.ball.dy = self.init_ball_yspeed
            if self.lives > 0:
                self.ball.hitbox.center = width * random.random(), height / 3
        if self.lives > 0:
            index = self.ball.hitbox.collidelist(self.wall.get_hitboxes())
            if index != -1:
                if self.ball.hitbox.center[0] > self.wall.bricks[index].hitbox.right \
                        or self.ball.hitbox.center[0] < self.wall.bricks[index].hitbox.left:
                    self.ball.dx *= -1
                else:
                    self.ball.dy *= -1
                self.wall.bricks[index:index + 1] = []
                self.score += 1

            hit_paddle = self.paddle.reflect_ball_if_hit(self.ball)
            if hit_paddle:
                self.num_times_hit_paddle += 1
            self.ball.move()

        self.screen.fill(bgcolor)
        if self.lives <= 0:
            self.game_over = True
            msgrect = self.game_over_msg.get_rect()
            msgrect = msgrect.move(width / 2 - (msgrect.center[0]), height / 3)
            self.screen.blit(self.game_over_msg, msgrect)
        lives_msg = pygame.font.Font(None, 40).render("Lives: " + str(self.lives), True, (0, 255, 255), bgcolor)
        lives_msg_rect = lives_msg.get_rect()
        lives_msg_rect = lives_msg_rect.move(0, 0)
        self.screen.blit(lives_msg, lives_msg_rect)
        scoretext = pygame.font.Font(None, 40).render("Score: " + str(self.score), True, (0, 255, 255), bgcolor)
        scoretextrect = scoretext.get_rect()
        scoretextrect = scoretextrect.move(width - scoretextrect.right, 0)
        self.screen.blit(scoretext, scoretextrect)

        for i in range(0, len(self.wall.bricks)):
            self.screen.blit(self.wall.bricks[i].image, self.wall.bricks[i].hitbox)

        if not self.wall.bricks:
            self.wall.build_wall()
            self.ball.dx = self.init_ball_xspeed
            self.ball.dy = self.init_ball_yspeed
            self.ball.hitbox.center = width / 2, height / 3

        self.screen.blit(self.ball.image, self.ball.hitbox)
        self.screen.blit(self.paddle.image, self.paddle.hitbox)

    def reset(self):
        self.__init__(self.screen)
