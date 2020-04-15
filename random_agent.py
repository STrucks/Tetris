from abstract_agent import AbstractAgent
import numpy as np
from game_enums import Actions

class RandomAgent(AbstractAgent):

    def move(self, game):
        return np.random.choice(list(Actions), p=[0.25, 0.25, 0.25, 0.25])