from brick import Brick


class Wall(object):
    def __init__(self, width):
        self.bricks = []
        self.brick_length = Brick().hitbox.right - Brick().hitbox.left
        self.brick_height = Brick().hitbox.bottom - Brick().hitbox.top
        self.build_wall(width)

    def build_wall(self, width):
        xpos = 0
        ypos = 60
        adj = 0
        for i in range(0, 52):
            if xpos > width:
                if adj == 0:
                    adj = self.brick_length / 2
                else:
                    adj = 0
                xpos = -adj
                ypos += self.brick_height
            new_brick = Brick()
            self.bricks.append(new_brick)
            self.bricks[i].hitbox = self.bricks[i].hitbox.move(xpos, ypos)
            xpos = xpos + self.brick_length

    def get_hitboxes(self):
        hitboxes = []
        for i in range(0, len(self.bricks)):
            hitboxes.append(self.bricks[i].hitbox)
        return hitboxes

    def get_num_bricks(self):
        return len(self.bricks)
