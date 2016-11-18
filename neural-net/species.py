import uuid
import random
from connection import Connection


class Species(object):
    def __init__(self, generation, breakout_model):
        self.genome = generation
        self.inputs = []
        self.outputs = []
        self.breakout_model = breakout_model
        # species id format: species-generation:{self.generation}-{uuid}
        self.id = "species-generation:" + self.genome + "-" + uuid.uuid4()
        self.fitness = 0

    def add_input(self, input_node):
        self.inputs.append(input_node)

    def add_output(self, output_node):
        self.outputs.append(output_node)

    def set_inputs(self, inputs):
        self.inputs = inputs

    def set_outputs(self, outputs):
        self.outputs = outputs

    def num_inputs(self):
        return len(self.inputs)

    def num_outputs(self):
        return len(self.outputs)

    def calculate_fitness(self):
        # fitness is essentially the average score per time ball hit paddle; perfect fitness would be {num_bricks} / 1
        self.fitness = self.breakout_model.score / self.breakout_model.num_times_hit_paddle
        return self.fitness

    def init_connections(self):
        """
        Assign random connections for a random number of nodes.
        :return:
        """
        num_conns_to_make = random.randint(0, 2 * len(self.inputs))
        for i in range(0, num_conns_to_make):
            input_index = random.randint(0, len(self.inputs))
            output_index = random.randint() % 2
            # Connection __init__ function adds itself to the connections list for the specified input and output nodes
            Connection(self.inputs[input_index], self.outputs[output_index])

    def get_all_connections(self):
        """
        Get all the connections associate with this specimen.
        :return: the list of all connections associated with this specimen.
        """
        conns = []
        for input_node in self.inputs:
            conns.extend(input_node.connections)
