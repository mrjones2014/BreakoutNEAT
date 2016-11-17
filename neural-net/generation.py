from node import Node
from output_node import OutputNode
from input_node import InputNode


class Generation(object):
    def __init__(self, breakout_model):
        self.breakout_model = breakout_model
        self.input_nodes = []
        for brick in self.breakout_model.wall.bricks:
            self.input_nodes.append(InputNode(brick.get_center))
        self.input_nodes.append(InputNode(self.breakout_model.paddle.get_center))
        self.output_nodes = [
            OutputNode(self.breakout_model.paddle.move_left()), OutputNode(self.breakout_model.paddle.move_right())
        ]
