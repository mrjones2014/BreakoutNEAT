from node import Node


class OutputNode(Node):
    def __init__(self, act_function):
        super(OutputNode, self).__init__()
        self.act_function = act_function
        self.weight = 0.0
        self.update_weight()

    def update_weight(self):
        total = 0.0
        for conn in self.connections:
            total += conn.weight + conn.input.weight
        self.weight = total
        return total

    def act(self):
        """
        Perform the action associated with this output.
        :return: void
        """
        self.act_function()
