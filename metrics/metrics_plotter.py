import os
import matplotlib.pyplot as plt
import re
from decimal import Decimal


def generate_graphs():
    # get list of file names in current directory other than this Python file
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f != 'metrics_plotter.py']
    for filename in files:
        with open(filename, 'r') as curr_file:
            lines = tuple(curr_file)
            graph_name = str(lines[0])
            gen_num_points = []
            fitness_points = []
            for i in range(1, len(lines)):
                gen_num_points.append(i - 1)
                fitness_points.append(Decimal(lines[i]))
            plt.plot(gen_num_points, fitness_points)
            plt.ylabel('Fitness')
            plt.xlabel('Generation Number')
            plt.title(graph_name)
            graph_file_name = re.sub('\s', '_', graph_name) + '.png'
            plt.savefig(graph_file_name, bbox_inches='tight')
            plt.clf()

if __name__ == "__main__":
    generate_graphs()
