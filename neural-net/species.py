import uuid


class Species(object):
    def __init__(self, generation, breakout_model):
        self.genome = generation
        self.inputs = []
        self.outputs = []
        self.breakout_model = breakout_model
        # species id format: species-generation:{self.generation}-{uuid}
        self.id = "species-generation:" + self.genome + "-" + uuid.uuid4()
        self.fitness = 0

    def num_inputs(self):
        return len(self.inputs)

    def num_outputs(self):
        return len(self.outputs)

    def calculate_fitness(self):
        # fitness is essentially the average score per time ball hit paddle; perfect fitness would be {num_bricks} / 1
        self.fitness = self.breakout_model.score / self.breakout_model.num_times_hit_paddle
        return self.fitness
