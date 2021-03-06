from __future__ import division
from node import Node
import math
import random
from neural_net_params import *


class OutputNode(Node):
    def __init__(self, act_function, index=-1):
        super(OutputNode, self).__init__()
        random.seed()
        self.act_function = act_function
        self.weight = 0.0
        self.update_weight()
        self.index = index

    def update_weight(self):
        total = 0.0
        for conn in self.connections:
            total += conn.input.update_weight()
        self.weight = OutputNode.sigmoid_activation_function(total)
        return self.weight

    @staticmethod
    def sigmoid_activation_function(value):
        """
        Sigmoid activation function for the genetic algorithm outputs.
        :param value: value on which to perform the Sigmoid activation.
        :return: Decimal type
        """
        try:
            return 1 / (1 + math.exp(value))
        except OverflowError:
            return random.choice([FALLBACK_WEIGHT_LOW, FALLBACK_WEIGHT_HIGH])

    def do_act(self):
        """
        Perform the action associated with this output.
        :return: void
        """
        self.act_function()

    def is_same(self, other):
        """
        Determine whether this OutputNode is unique or the same as the OutputNode provided as a parameter.
        :param other: OutputNode to check uniqueness against.
        :return: True if the node is *NOT* unique, False otherwise.
        """
        if self.act_function == other.act_function:
            return True
        else:
            return False
