from __future__ import division
from neural_net_params import *
from breakout_game.breakout import Breakout
from breakout_game.game_params import *
import pygame
from generation import Generation
from species import Species
import sys


class Experiment(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.key.set_repeat(1, 30)
        self.breakout_game = Breakout(self.screen)
        self.generations = []

    def run(self, seed_gen=None):
        print "Running generation 0..."
        if seed_gen is None:
            first_gen = Generation(self.breakout_game, 0)
        else:
            first_gen = seed_gen
        first_gen.run_and_evaluate()
        print "    Average fitness in generation 0: " + str(first_gen.avg_fitness())
        first_ancestor = first_gen.epoch()
        curr_gen = first_gen.evolve_from_ancestor(first_ancestor)
        print "Average fitness in generation 1: " + str(curr_gen.avg_fitness())
        last_individual_xml = first_ancestor.to_xml_str()
        for i in range(1, NUM_GENERATIONS):
            print "Running generation " + str(i) + "..."
            curr_gen.run_and_evaluate()
            print "    Average fitness in generation " + str(i) + ": " + str(curr_gen.avg_fitness())
            next_ancestor = curr_gen.epoch()
            last_individual_xml = next_ancestor.to_xml_str()
            next_gen = curr_gen.evolve_from_ancestor(next_ancestor)
            curr_gen = next_gen
        save_to_file = raw_input("Save speciation data (y/n): ")
        if save_to_file == "y" or save_to_file == "Y":
            filename = raw_input("Enter filename to write to: ")
            if not filename.endswith(".species"):
                filename += ".species"
            print "Writing speciation data to " + filename + ".species..."
            Species.save_state(filename, last_individual_xml)
            print "Done."

    def load_data(self, filename):
        if not filename.endswith(".species"):
            filename += ".species"
        if not filename.startswith(DATA_DIR):
            filename = DATA_DIR + filename
        try:
            with open(filename) as data_file:
                xml_str = data_file.read()
                seed_species = Species.parse(xml_str, self.breakout_game)
                seed_gen = Generation.seed(seed_species, 0)
            return seed_gen
        except Exception, e:
            print "FATAL: File does not exist or is corrupted."
            print e
            sys.exit(-1)

if __name__ == "__main__":
    seed = None
    experiment = Experiment()
    do_seed = raw_input("Load speciation data from file? (y/n): ")
    if do_seed == "y" or do_seed == "Y":
        file_name = raw_input("Enter name of species file: ")
        seed = experiment.load_data(file_name)
    experiment.run(seed)
