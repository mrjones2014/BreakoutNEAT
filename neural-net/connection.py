import random
from neural_net_params import *


class Connection(object):
    def __init__(self, input_node, output_node):
        self.weight = random.randrange(MIN_WEIGHT, MAX_WEIGHT)
        self.input = input_node
        self.output = output_node
        input_node.add_connection(self)
        output_node.add_connection(self)

    def is_same(self, other):
        """
        Determine whether this connection is unique or the same as the connection provided as a parameter.
        :param other: Connection to check uniqueness against.
        :return: True if connection is *NOT* unique, False if it *IS* unique.
        """
        if self.input == other.input and self.output == other.output:
            return True
        else:
            return False
