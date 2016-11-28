from __future__ import division
from neural_net_params import *
from breakout_game.breakout import Breakout
from breakout_game.game_params import *
import pygame
from generation import Generation


class Experiment(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.key.set_repeat(1, 30)
        self.breakout_game = Breakout(self.screen)
        self.generations = []

    def run(self):
        print "Running generation 0..."
        first_gen = Generation(self.breakout_game, 0)
        first_gen.run_and_evaluate()
        print "    Average fitness in generation 0: " + str(first_gen.avg_fitness())
        first_ancestor = first_gen.epoch()
        curr_gen = first_gen.evolve_from_ancestor(first_ancestor)
        print "Average fitness in generation 1: " + str(curr_gen.avg_fitness())
        for i in range(1, NUM_GENERATIONS):
            print "Running generation " + str(i) + "..."
            curr_gen.run_and_evaluate()
            print "    Average fitness in generation " + str(i) + ": " + str(curr_gen.avg_fitness())
            next_ancestor = curr_gen.epoch()
            next_gen = curr_gen.evolve_from_ancestor(next_ancestor)
            curr_gen = next_gen

if __name__ == "__main__":
    experiment = Experiment()
    experiment.run()
