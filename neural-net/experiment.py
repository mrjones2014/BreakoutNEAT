from __future__ import division
from neural_net_params import *
from breakout_game.breakout import Breakout
from breakout_game.game_params import *
import pygame
from generation import Generation
from species import Species
import sys
import os
from session_logger import SessionLogger
from metrics import metrics_plotter


class Experiment(object):
    def __init__(self):
        pygame.init()
        self.screen = None
        self.breakout_game = None
        pygame.key.set_repeat(1, 30)
        self.generations = []
        self.logger = None
        self.current_best_species = None

    def initialize(self, event_logger):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.breakout_game = Breakout(self.screen)
        self.logger = event_logger

    def run(self, seed_gen=None):
        self.logger.log("Running generation 0...")
        if seed_gen is None:
            first_gen = Generation(self.breakout_game, 0)
        else:
            first_gen = seed_gen
        first_gen.run_and_evaluate(self.logger)
        avg_fitness = first_gen.avg_fitness()
        self.logger.log("    Average fitness in generation 0: " + DECIMAL_FORMAT_STR.format(avg_fitness))
        first_ancestor = first_gen.epoch()
        self.logger.log("    Highest fitness in generation 0: " + DECIMAL_FORMAT_STR.format(first_gen.highest_fitness))
        metrics_dict = Experiment.build_metrics_dict([avg_fitness, first_gen.highest_fitness])
        SessionLogger.log_metrics(metrics_dict)
        curr_gen = first_gen.evolve_from_ancestor(first_ancestor)
        last_individual_xml = first_ancestor.to_xml_str()
        for i in range(1, NUM_GENERATIONS):
            self.logger.log("Running generation " + str(i) + "...")
            curr_gen.run_and_evaluate(self.logger)
            avg_fitness = curr_gen.avg_fitness()
            self.logger.log("    Average fitness in generation " + str(i) + ": " +
                            DECIMAL_FORMAT_STR.format(avg_fitness))

            next_ancestor = curr_gen.epoch()

            self.logger.log("    Highest fitness in generation " + str(i) + ": " +
                            DECIMAL_FORMAT_STR.format(curr_gen.highest_fitness))
            metrics_dict = Experiment.build_metrics_dict([avg_fitness, curr_gen.highest_fitness])
            SessionLogger.log_metrics(metrics_dict)

            if self.current_best_species is None or next_ancestor.fitness > self.current_best_species.fitness:
                self.current_best_species = next_ancestor
            last_individual_xml = next_ancestor.to_xml_str()
            next_gen = curr_gen.evolve_from_ancestor(self.current_best_species)
            curr_gen = next_gen
        pygame.quit()
        if SAVE_SPECIATION_DATA:
            self.logger.log("Writing speciation data to file: " + SPECIATION_DATA_FILE)
            Species.save_state(SPECIATION_DATA_FILE, last_individual_xml)
            self.logger.log("Done writing speciation data to file: " + SPECIATION_DATA_FILE)
        if GENERATE_UPDATED_METRICS:
            metrics_plotter.generate_graphs()

    def load_data(self, filename):
        if not filename.endswith(".species"):
            filename += ".species"
        if not filename.startswith(SPECIATION_DATA_DIR):
            filename = SPECIATION_DATA_DIR + filename
        try:
            with open(filename) as data_file:
                xml_str = data_file.read()
                seed_species = Species.parse(xml_str, self.breakout_game)
                seed_gen = Generation.seed(seed_species, 0)
            return seed_gen
        except Exception, e:
            self.logger.log("FATAL: File does not exist or is corrupted: " + filename)
            self.logger.log(str(e))
            sys.exit(-1)

    @staticmethod
    def build_metrics_dict(data_points):
        if len(data_points) != len(METRICS_FILES):
            logger.log("FATAL: Number of data points does not match number of metrics files.")
            sys.exit(-1)
        else:
            dict = {}
            for i in range(0, len(METRICS_FILES)):
                dict[METRICS_FILES[i]] = data_points[i]
            return dict

if __name__ == "__main__":
    logger = SessionLogger(LOG_DIR + "events.log", True)
    logger.log("Session start.")
    seed = None
    experiment = Experiment()
    if DO_SEED:
        logger.log("Attempting to load speciation data from file: " + SPECIATION_DATA_FILE)
        logger.log("Initializing Experiment...")
        experiment.initialize(logger)
        seed = experiment.load_data(SPECIATION_DATA_FILE)
        logger.log("Successfully loaded speciation data from file: " + SPECIATION_DATA_FILE)
    else:
        logger.log("Initializing Experiment...")
        experiment.initialize(logger)
    logger.log("Running Experiment...")
    experiment.run(seed)
    logger.log("Experiment terminated cleanly." + os.linesep + os.linesep)
