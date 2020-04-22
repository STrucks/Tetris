import numpy as np

from Agents.abstract_agent import AbstractAgent
from game_enums import Actions


class RandomAgent(AbstractAgent):

    def move(self, game):
        return np.random.choice(list(Actions), p=[0.25, 0.25, 0.25, 0.25])