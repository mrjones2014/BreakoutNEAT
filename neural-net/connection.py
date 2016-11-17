import random
from neural_net_params import *


class Connection(object):
    def __init__(self, input_node, output_node):
        self.weight = random.randrange(MIN_WEIGHT, MAX_WEIGHT)
        self.input = input_node
        self.output = output_node
        input_node.add_connection(self)
        output_node.add_connection(self)
