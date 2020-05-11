from nn_models import GA_MLP
from Agents.abstract_agent import AbstractAgent
import numpy as np
from game_enums import Actions

class Individuum(AbstractAgent):

    def __init__(self):
        self.window_shape = (5, 4)
        self.window_width = int((self.window_shape[0]-1)/2)
        self.nn = GA_MLP(in_nodes=self.window_shape[0]*self.window_shape[1] + 7 + 2, out_nodes=4)

    def move(self, game):
        field, blocks, active_block = game.get_representations()
        sight = self.get_sight(active_block, field)
        features = self.get_features(active_block, field)
        nn_input = np.concatenate((sight, features), axis=1)
        action_distr = self.nn.forward(nn_input)
        action_index = action_distr.argmax()
        return Actions(action_index)

    def get_sight(self, block, field):
        sight = np.zeros(shape=self.window_shape)
        for index, field_row in enumerate(field[block.anchor[0]:block.anchor[0]+self.window_shape[1]]):
            left = block.anchor[1]-self.window_width
            right = block.anchor[1]+self.window_width
            if left < 0:
                padding_left = np.abs(left)
                for i, value in enumerate(field_row[0:right]):
                    sight[index, padding_left+i] = value
            elif right > field.shape[1]:
                sight[index, 0:field.shape[1] - left] = field_row[left:field.shape[1]]
            else:

                sight[index, 0:right-left] = field_row[left:right]
        sight = np.reshape(sight, (1, self.window_shape[0]*self.window_shape[1]))
        return sight

    def get_features(self, block, field):
        features = np.zeros(shape=(1, 9))
        # first 7 features are on hot encoding of the shape:
        features[0, block.shape_id] = 1
        # last 2 are distance to highest point:
        y_high_index = 0
        x_high_index = len(field)
        for index, row in enumerate(field):
            row_ones_index = np.where(row == 1)
            if len(row_ones_index[0]) > 0:
                y_high_index = row_ones_index[0][0]
                x_high_index = index
                break
        dist_to_highest = np.sqrt(np.power(block.get_anchor()[0]-x_high_index, 2) + np.power(block.get_anchor()[1]-y_high_index, 2))
        features[0, 7] = dist_to_highest
        # TODO do that
        return features

    def clone(self):
        copy = Individuum()
        copy.nn = copy.nn.clone()
        return copy
