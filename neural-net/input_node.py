from node import Node


class InputNode(Node):
    def __init__(self, input_update_function):
        super(InputNode, self).__init__()
        self.update_func = input_update_function
        self.weight = self.update_func()

    def update_weight(self):
        if self.update_func:
            self.weight += (self.update_func() * self.get_sum_connections_weight())

    def is_same(self, other):
        """
        Determine whether this InputNode is unique or the same as the InputNode provided as a parameter.
        :param other: InputNode to check uniqueness against.
        :return: True if the node is *NOT* unique, False otherwise.
        """
        if self.update_func == other.update_func:
            return True
        else:
            return False
