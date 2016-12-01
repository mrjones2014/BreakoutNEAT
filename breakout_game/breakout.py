from __future__ import division
import pygame
from paddle import Paddle
from ball import Ball
from wall import Wall
from game_params import *
import random
import numpy


class Breakout(object):
    def __init__(self, screen):
        # fields needed for the game itself
        self.game_over_msg = pygame.font.Font(None, 70).render("Game Over", True, (0, 255, 255), bgcolor)
        self.game_over = False
        self.time = 0
        self.paddle = Paddle()
        self.paddle.hitbox.move((width / 2) - (self.paddle.hitbox.right / 2), height - 20)
        self.ball = Ball()
        self.ball.hitbox.center = (width / 2, height / 2)
        self.init_ball_x_speed = 4
        self.init_ball_y_speed = 4
        self.ball.dx = self.init_ball_x_speed
        self.ball.dy = self.init_ball_y_speed
        self.wall = Wall()
        self.score = 0
        self.lives = init_lives
        self.screen = screen
        self.arrow_char = " - "

        # additional data for the fitness evaluation
        self.total_paddle_offset_from_center = 0
        self.avg_paddle_offset_from_center = 0
        self.num_times_hit_paddle = 0
        self.hits_per_life = []
        self.stale = False
        self.stale_frame_count = 0
        self.prev_ball_location = None

    def update(self):
        if not self.game_over:
            if self.prev_ball_location is not None:
                if numpy.abs(self.prev_ball_location[0] - self.ball.hitbox.center[0]) < 5 \
                        or numpy.abs(self.prev_ball_location[1] - self.ball.hitbox.center[1]) < 5:
                    self.stale_frame_count += 1
                else:
                    self.stale_frame_count = 0
            if self.stale_frame_count > max_stale_frames:
                self.stale = True
                self.ball.cause_miss()
            else:
                self.stale = False
            self.prev_ball_location = (self.ball.hitbox.center[0], self.ball.hitbox.center[1])
            self.time += 1

            self.total_paddle_offset_from_center += numpy.abs((width / 2) - self.paddle_center())
            self.avg_paddle_offset_from_center = self.total_paddle_offset_from_center / self.time

        if self.ball.hitbox.top > height and self.lives > 0:
            index = init_lives - self.lives
            self.lives -= 1
            if index == 0:
                self.hits_per_life.append(self.num_times_hit_paddle)
            else:
                self.hits_per_life.append(self.num_times_hit_paddle - self.hits_per_life[index - 1])
            self.ball.dx = self.init_ball_x_speed
            if random.random() > 0.5:
                self.ball.dx *= -1
            self.ball.dy = self.init_ball_y_speed
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
            msg_rect = self.game_over_msg.get_rect()
            msg_rect = msg_rect.move(width / 2 - (msg_rect.center[0]), height / 3)
            self.screen.blit(self.game_over_msg, msg_rect)

        lives_msg = pygame.font.Font(None, 40).render("Lives: " + str(self.lives), True, (0, 255, 255), bgcolor)
        lives_msg_rect = lives_msg.get_rect()
        lives_msg_rect = lives_msg_rect.move(0, 0)
        self.screen.blit(lives_msg, lives_msg_rect)

        arrow_indicator = pygame.font.Font(None, 40).render("Output: " + self.arrow_char, True, (0, 255, 255), bgcolor)
        arrow_rect = arrow_indicator.get_rect()
        arrow_rect = arrow_rect.move((width / 2) - (arrow_rect.right / 2), 0)
        self.screen.blit(arrow_indicator, arrow_rect)

        score_text = pygame.font.Font(None, 40).render("Score: " + str(self.score), True, (0, 255, 255), bgcolor)
        score_text_rect = score_text.get_rect()
        score_text_rect = score_text_rect.move(width - score_text_rect.right, 0)
        self.screen.blit(score_text, score_text_rect)

        for i in range(0, len(self.wall.bricks)):
            self.screen.blit(self.wall.bricks[i].image, self.wall.bricks[i].hitbox)

        if not self.wall.bricks:
            self.wall.build_wall()
            self.ball.dx = self.init_ball_x_speed
            self.ball.dy = self.init_ball_y_speed
            self.ball.hitbox.center = width / 2, height / 3
            self.paddle.__init__()

        self.screen.blit(self.ball.image, self.ball.hitbox)
        self.screen.blit(self.paddle.image, self.paddle.hitbox)

    def move_paddle_right(self):
        self.arrow_char = " ->"
        self.paddle.move_right()

    def move_paddle_left(self):
        self.arrow_char = "<- "
        self.paddle.move_left()

    def move_paddle_none(self):
        self.arrow_char = " - "

    def paddle_center(self):
        return self.paddle.hitbox.center[0]

    def get_ball_center_x(self):
        return self.ball.hitbox.center[0]

    def get_ball_center_y(self):
        return self.ball.hitbox.center[1]

    def get_ball_dx(self):
        return self.ball.dx

    def get_ball_dy(self):
        return self.ball.dy

    def get_ball_velocity_magnitude(self):
        return numpy.sqrt((self.ball.dx * self.ball.dx) + (self.ball.dy * self.ball.dy))

    def reset(self):
        self.__init__(self.screen)
