from __future__ import division
from output_node import OutputNode
from input_node import InputNode
from neural_net_params import *
from species import Species
from decimal import Decimal
import pygame
import sys


class Generation(object):
    def __init__(self, breakout_model, generation_num):
        self.highest_fitness = None
        self.number = generation_num
        self.individuals = []
        self.breakout_model = breakout_model
        self.epoch_occurred = False
        self.evolved_child = None
        for i in range(0, NUM_INDIVIDUALS_PER_GENERATION):
            individual = Species(self.number, i, self.breakout_model)
            self.init_individual(individual)
            self.individuals.append(individual)

    def init_individual(self, individual):
        """
        Initialize an individual in a generation with input and output nodes and connections.
        :param individual: specimen to initialize.
        :return: void
        """
        individual.set_inputs([
            InputNode(self.breakout_model.paddle_center, 0), InputNode(self.breakout_model.get_ball_center, 1),
            InputNode(self.breakout_model.get_ball_dx, 2), InputNode(self.breakout_model.get_ball_dy, 3)
        ])
        individual.set_outputs([
            OutputNode(self.breakout_model.move_paddle_left, 0), OutputNode(self.breakout_model.move_paddle_right, 1),
            OutputNode(self.breakout_model.move_paddle_none, 2)
        ])
        individual.init_connections()

    def epoch(self):
        """
        Trigger an Epoch event; meant to be called at the end of a generation's last individual's game.
        Determine and breed the two most fit individuals and return the evolved child.
        Also resets the Breakout game model
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
        self.evolved_child = Species(self.number + 1, 0, self.breakout_model)
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
        self.evolved_child.mutate()
        self.epoch_occurred = True
        self.breakout_model.reset()
        return self.evolved_child

    def run_and_evaluate(self, logger):
        self.breakout_model.reset()
        for individual in self.individuals:
            while not self.breakout_model.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                individual.update_all_node_weights()
                individual.act()
                self.breakout_model.update()
                pygame.display.flip()
            individual.calculate_fitness()
            if self.highest_fitness is None or individual.fitness > self.highest_fitness:
                self.highest_fitness = individual.fitness
            logger.log("        " + str(individual.id) + " fitness = " + str(individual.fitness))
            self.breakout_model.reset()

    def evolve_from_ancestor(self, ancestor):
        """
        Evolve into a new generation from a "seed" individual.
        The generation's evolved child should be passed as an ancestor after the Epoch.
        :param ancestor: the ancestor individual to evolve a new generation from.
        :return: the next, evolved generation
        """
        next_gen = Generation(self.breakout_model, self.number + 1)
        next_gen.breakout_model.reset()
        next_gen.individuals = []
        next_gen.epoch_occurred = False
        next_gen.evolved_child = None
        for i in range(0, NUM_INDIVIDUALS_PER_GENERATION):
            individual = Species.copy(self.number + 1, i, ancestor)
            next_gen.init_individual(individual)
            next_gen.individuals.append(individual)
        return next_gen

    def avg_fitness(self):
        total = 0.0
        total = Decimal(total)
        for individual in self.individuals:
            total += Decimal(individual.fitness)
        return Decimal(total / Decimal(len(self.individuals)))

    @staticmethod
    def compare_individuals(ind_1, ind_2):
        """
        Compare individuals based on their fitness.
        :param ind_1: specimen 1 to compare
        :param ind_2: specimen 2 to compare
        :return: the integer resulting from comparing the two specimens
        """
        return int(ind_1.fitness - ind_2.fitness)

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

    @staticmethod
    def seed(ancestor, generation_num):
        new_gen = Generation(ancestor.breakout_model, generation_num)
        new_gen.number = generation_num
        new_gen.individuals = []
        new_gen.breakout_model = ancestor.breakout_model
        new_gen.epoch_occurred = False
        new_gen.evolved_child = None
        for i in range(0, NUM_INDIVIDUALS_PER_GENERATION):
            individual = Species.copy(generation_num, ancestor.individual_number, ancestor)
            new_gen.init_individual(individual)
            new_gen.individuals.append(individual)
