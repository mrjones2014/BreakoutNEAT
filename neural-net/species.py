from __future__ import division
from neural_net_params import *
import random
from connection import Connection
import numpy
from decimal import Decimal
from lxml import etree
from input_node import InputNode
from output_node import OutputNode


class Species(object):
    def __init__(self, generation, individual_num, breakout_model):
        self.genome = generation
        self.inputs = []
        self.outputs = []
        self.breakout_model = breakout_model
        self.individual_number = individual_num
        # species id format: species-generation:{self.generation}-{self.individual_number}
        self.id = "species#generation:" + str(self.genome) + "-individual:" + str(self.individual_number)
        self.fitness = 0.0
        self.fitness = Decimal(self.fitness)

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
        self.fitness = self.breakout_model.score
        if self.breakout_model.avg_paddle_offset != 0:
            self.fitness -= numpy.log10(self.breakout_model.avg_paddle_offset) * 0.1
        return self.fitness

    def init_connections(self):
        """
        Assign random connections for a random number of nodes.
        :return: void
        """
        num_conns_to_make = random.randint(0, 2 * len(self.inputs))
        for i in range(0, num_conns_to_make):
            input_index = random.randint(0, len(self.inputs) - 1)
            output_index = random.randint(0, 100) % 2
            # Connection __init__ function adds itself to the connections list for the specified input and output nodes
            Connection(self.inputs[input_index], self.outputs[output_index])

    def get_all_connections(self):
        """
        Get all the connections associated with this specimen.
        :return: the list of all connections associated with this specimen.
        """
        conns = []
        for input_node in self.inputs:
            conns.extend(input_node.connections)
        return conns

    def update_all_node_weights(self):
        """
        Calls update on each input and output node of this species.
        :return:
        """
        for input_node in self.inputs:
            input_node.update_weight()
        for output_node in self.outputs:
            output_node.update_weight()

    def mutate(self):
        """
        Mutate the species. Small chance of mutation being completely random, otherwise changes weights within a range
        specified by MAX_MUTATION in neural_net_params.py. Small chance of adding new connection during mutation.
        If new connection is added, chance of adding 2 connections instead of just one.
        :return: void
        """
        randomly_mutate = random.uniform(0, 100) % 33 == 0
        if randomly_mutate:
            for conn in self.get_all_connections():
                conn.weight = random.uniform(MIN_CONNECTION_WEIGHT, MAX_CONNECTION_WEIGHT)
        else:
            for conn in self.get_all_connections():
                diff = random.uniform(-1 * MAX_MUTATION, MAX_MUTATION)
                if diff < 0:
                    conn.weight = max(MIN_CONNECTION_WEIGHT, diff)
                elif diff > 0:
                    conn.weight = min(MAX_CONNECTION_WEIGHT, diff)
        mutate_new_connection = random.uniform(0, 100) % 20 == 0
        if mutate_new_connection:
            input_index = random.randint(0, len(self.inputs) - 1)
            output_index = random.randint(0, 100) % 2
            Connection(self.inputs[input_index], self.outputs[output_index])
            if bool(random.getrandbits(1)):
                input_index = random.randint(0, len(self.inputs) - 1)
                output_index = random.randint(0, 100) % 2
                Connection(self.inputs[input_index], self.outputs[output_index])

    def act(self):
        """
        Calls act() on the output node with the greatest resultant weight.
        :return: void
        """
        self.update_all_node_weights()
        # print "output 0 weight: ", self.outputs[0].weight
        # print "output 1 weight: ", self.outputs[1].weight
        if self.outputs[0].weight > self.outputs[1].weight:
            self.outputs[0].do_act()
        else:
            self.outputs[1].do_act()

    def to_xml_str(self):
        root = etree.Element("species")
        genome = etree.Element("genome")
        genome.text = str(self.genome)
        root.append(genome)
        conns = etree.Element("connection_list")

        for conn in self.get_all_connections():
            conn_node = etree.Element("connection")

            in_node = etree.Element("input")
            in_node.text = str(conn.input.index)

            out_node = etree.Element("output")
            out_node.text = str(conn.output.index)

            conn_node.append(in_node)
            conn_node.append(out_node)

            conns.append(conn_node)

        root.append(conns)

        xml_str = etree.tostring(root, pretty_print=True)
        return xml_str

    @staticmethod
    def save_state(filename, xml_str):
        if not filename.endswith(".species"):
            filename += ".species"
        if not filename.startswith(DATA_DIR):
            filename = DATA_DIR + filename
        with open(filename, "w") as species_file:
            species_file.write(xml_str)

    @staticmethod
    def node_weight_comparator(n1, n2):
        return int(n1.weight) - int(n2.weight)

    @staticmethod
    def copy(genome, individual_num, other_species):
        new_species = Species(genome, individual_num, other_species.breakout_model)
        new_species.inputs = other_species.inputs
        new_species.outputs = other_species.outputs
        new_species.id = "species#generation:" + str(genome) + "-individual:" + str(individual_num)
        new_species.fitness = 0
        return new_species

    @staticmethod
    def parse(ancestor_xml, breakout_model):
        root = etree.fromstring(ancestor_xml)
        genome = int(root.find("genome").text)
        new_spec = Species(genome, 0, breakout_model)
        conn_list = root.find("connection_list").findall("connection")
        new_spec.set_inputs([
            InputNode(breakout_model.paddle_center, 0), InputNode(breakout_model.get_ball_center, 1)
        ])
        new_spec.set_outputs([
            OutputNode(breakout_model.move_paddle_left, 0), OutputNode(breakout_model.move_paddle_right, 1)
        ])

        for conn_xml in conn_list:
            input_index = int(conn_xml.find("input").text)
            output_index = int(conn_xml.find("output").text)
            Connection(new_spec.inputs[input_index], new_spec.outputs[output_index])
        return new_spec
