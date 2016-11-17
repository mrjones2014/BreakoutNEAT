import pygame


class Brick(object):
    def __init__(self):
        self.image = pygame.image.load("../assets/brick.png")
        self.hitbox = self.image.get_rect()
        self.broken = False

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

            self.broken = True
