from nn_models import GA_MLP
from Agents.abstract_agent import AbstractAgent
import numpy as np
from game_enums import Actions

class Individuum(AbstractAgent):

    def __init__(self):
        self.window_size = 5

        self.nn = GA_MLP(in_nodes=self.window_size*self.window_size + 3, out_nodes=4)

    def move(self, game):
        field, blocks, active_block = game.get_representations()
        nn_input = np.random.rand(1, self.window_size*self.window_size + 3)
        action_distr = self.nn.forward(nn_input)
        action_index = action_distr.argmax()
        return Actions(action_index)