import numpy as np


class AbstractAgent:

    def __init__(self):
        pass

    def move(self, field, inactive_blocks, active_block):
        raise NotImplementedError()
