from output_node import OutputNode
from input_node import InputNode
from neural_net_params import *
from species import Species


class Generation(object):
    def __init__(self, breakout_model, generation_num):
        self.number = generation_num
        self.individuals = []
        self.breakout_model = breakout_model
        self.epoch_occurred = False
        self.evolved_child = None
        for i in range(0, NUM_INDIVIDUALS_PER_GENERATION):
            individual = Species(self.number, self.breakout_model)
            self.init_individual(individual)
            self.individuals.append(individual)

    def init_individual(self, individual):
        """
        Initialize an individual in a generation with input and output nodes and connections.
        :param individual: specimen to initialize.
        :return: void
        """
        for brick in self.breakout_model.wall.bricks:
            individual.add_input(InputNode(brick.get_center))
        individual.add_input(InputNode(self.breakout_model.paddle.get_center))
        individual.set_outputs([
            OutputNode(self.breakout_model.paddle.move_left()), OutputNode(self.breakout_model.paddle.move_right())
        ])
        individual.init_connections()

    def epoch(self):
        """
        Trigger an Epoch event; meant to be called at the end of a generation's last individual's game.
        Determine and breed the two most fit individuals and return the evolved child.
        Also resets the Breakout game model.
        :return: the child evolved from breeding the two most fit individuals in the generation.
        """
        # if the epoch has already happened, the evolved child has already been created; return it.
        if self.epoch_occurred:
            return self.evolved_child
        # otherwise, evolve the child.
        for individual in self.individuals:
            individual.calculate_fitness()
        sorted_by_fitness = sorted(self.individuals, Generation.compare_individuals)
        specimen_1 = sorted_by_fitness[0]
        specimen_2 = sorted_by_fitness[1]

        s1_conns = specimen_1.get_all_connections()
        s2_conns = specimen_2.get_all_connections()
        new_connections = Generation.breed_connections(s1_conns, s2_conns)
        self.evolved_child = Species(self.number + 1, self.breakout_model)
        for conn in new_connections:
            input_is_duplicate = False
            output_is_duplicate = False
            for input_node in self.evolved_child.inputs:
                if conn.input.is_same(input_node):
                    input_is_duplicate = True
            for output_node in self.evolved_child.outputs:
                if conn.output.is_same(output_node):
                    output_is_duplicate = True
            if not input_is_duplicate:
                self.evolved_child.add_input(conn.input)
            if not output_is_duplicate:
                self.evolved_child.add_output(conn.output)
        self.evolved_child.init_connections()
        self.epoch_occurred = True
        self.breakout_model.reset()
        return self.evolved_child

    def run_and_evaluate(self):
        for individual in self.individuals:
            while not self.breakout_model.game_over:
                individual.update_all_node_weights()
                individual.act()
                self.breakout_model.update()
            individual.calculate_fitness()
            self.breakout_model.reset()

    @staticmethod
    def compare_individuals(ind_1, ind_2):
        """
        Compare individuals based on their fitness.
        :param ind_1: specimen 1 to compare
        :param ind_2: specimen 2 to compare
        :return: the integer resulting from comparing the two specimens
        """
        return ind_1.fitness - ind_2.fitness

    @staticmethod
    def breed_connections(s1_conns, s2_conns):
        """
        Create a new list of connections made up of only the *UNIQUE* connections from each specimen.
        :param s1_conns: list of connections from specimen 1
        :param s2_conns: list of connections from specimen 2
        :return: list of resultant connections after breeding
        """
        connections = []
        connections.extend(s1_conns)
        for conn1 in s2_conns:
            is_duplicate = False
            for conn2 in connections:
                if conn1.is_same(conn2):
                    is_duplicate = True
            if not is_duplicate:
                connections.append(conn1)
        return connections
