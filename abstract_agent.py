import numpy as np


class AbstractAgent:

    def __init__(self):
        pass

    def move(self, game):
        raise NotImplementedError()
