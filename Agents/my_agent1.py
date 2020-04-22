import operator
from copy import deepcopy

import numpy as np

from Agents.abstract_agent import AbstractAgent
from config_loader import config
from game_enums import Actions


class MyAgent1(AbstractAgent):

    def __init__(self):
        """
        This agent mainly searches over a large collection of possible gamestates. It will then choose the action that
        will yield the best gamestate
        """
        self.FIELD_WIDTH = config["FIELD-WIDTH"]
        self.FIELD_HEIGHT = config["FIELD-HEIGHT"]
        self.SEARCH_DEPTH = 3
        pass

    def move(self, game):
        """
        This function determines the next best move for the game
        :param game:
        :return:
        """
        field, blocks, active_block = game.get_representations()
        evaluations = {}
        successors = self.__get_successor_states(field, blocks, active_block)

        for action in successors.keys():
            field, blocks, active_block = successors[action]
            evaluations[action] = self.evaluate_successors(field, blocks, active_block, 0)

        return max(evaluations.items(), key=operator.itemgetter(1))[0]

    def evaluate_successors(self, field, blocks, active_block, depth):
        if depth >= self.SEARCH_DEPTH:
            return 0
        else:
            # evaluate current state:
            evaluation = self.__evaluate_field(field)*np.power(0.9, depth)

            # evaluate the children and take the max:
            successors = self.__get_successor_states(field, blocks, active_block)
            for action in successors.keys():
                field, blocks, active_block = successors[action]
                evaluation = max(evaluation, self.evaluate_successors(field, blocks, active_block, depth+1))
            return evaluation

    def __get_successor_states(self, field, blocks, active_block):
        successors = {}
        for action in list(Actions):
            field_copy, blocks_copy, active_block_copy = deepcopy(field), deepcopy(blocks), deepcopy(active_block)
            field_copy, blocks_copy, active_block_copy = self.apply_action(action, field_copy, blocks_copy, active_block_copy)
            field_copy, blocks_copy, active_block_copy = self.apply_physics(field_copy, blocks_copy, active_block_copy)
            successors[action] = [field_copy, blocks_copy, active_block_copy]
        return successors

    def __evaluate_field(self, field):
        """
        Gives a field a numerical score, that reflects the "goodness" of the state.

        We want:
        - very dense area at the bottom (TODO)
        - a complete row
        - all blocks as deep as possible
        :return: score
        """
        score = 0
        for index, row in enumerate(field):
            score += index*sum(row)
        return score

    def apply_action(self, action, field, blocks, active_block):
        x_anchor, y_anchor = active_block.get_anchor()
        if action == Actions.ROTATE:
            new_shape = active_block.rotate()
            # check if the new coords are out of bounds:
            new_coords = [[active_block.anchor[0] + x, active_block.anchor[1] + y] for [x, y] in new_shape]
            collide_flag = False
            for [x, y] in new_coords:
                if collide_flag:
                    continue
                if 0 <= x < self.FIELD_HEIGHT and 0 <= y < self.FIELD_WIDTH:
                    pass
                else:
                    collide_flag = True
            # check if the rotation collides with other blocks:
            for [x, y] in new_coords:
                for block in blocks:
                    if [x, y] in block.get_coords():
                        collide_flag = True
            if not collide_flag:
                active_block.set_shape(new_shape)
                #logging.debug("rotated block successfully")
        else:
            movement = self.__convert_action2move(action)
            new_y_anchor = y_anchor + movement
            # check boundaries:
            if 0 <= new_y_anchor <= self.FIELD_WIDTH - active_block.WIDTH:
                collide_flag = False
                for [x, y] in active_block.get_shape():
                    if collide_flag:
                        continue
                    for b in blocks:
                        occupied_coords = b.get_coords()
                        if [x_anchor + x, new_y_anchor + y] in occupied_coords:
                            collide_flag = True

                if not collide_flag:
                    active_block.set_anchor(x_anchor, new_y_anchor)
            else:
                pass
        field = self.update_field(blocks, active_block)
        return field, blocks, active_block

    def apply_physics(self, field, blocks, active_block):
        x_anchor, y_anchor = active_block.get_anchor()
        # check if block hit the bottom:
        if x_anchor < self.FIELD_HEIGHT - active_block.HEIGHT:
            # check if active block would collide with another block
            collide_flag = False
            new_x_anchor = x_anchor + 1
            for [x, y] in active_block.get_shape():
                if collide_flag:
                    continue
                for b in blocks:
                    occupied_anchor_x, occupied_anchor_y = b.get_anchor()
                    occupied_coords = [[occupied_anchor_x + x_o, occupied_anchor_y + y_o] for x_o, y_o in b.get_shape()]
                    if [new_x_anchor + x, y_anchor + y] in occupied_coords:
                        return field, blocks, active_block
            if not collide_flag:
                active_block.set_anchor(new_x_anchor, y_anchor)
            else:
                blocks.append(active_block)
                field, blocks, active_block = self.check_complete_row(field, blocks, active_block)
        else:
            blocks.append(active_block)
            field, blocks, active_block = self.check_complete_row(field, blocks, active_block)
        field = self.update_field(blocks, active_block)
        return field, blocks, active_block


    def __convert_action2move(self, action:Actions):
        if action == Actions.RIGHT:
            return 1
        elif action == Actions.LEFT:
            return -1
        elif action == Actions.STAY:
            return 0
        else:
            return 0

    def check_complete_row(self, field, blocks, active_block):
        # check if there is a complete row:
        to_be_removed_rows = []
        field = self.update_field(blocks, active_block)
        for index, row in enumerate(field):
            if np.sum(row) == self.FIELD_WIDTH:
                to_be_removed_rows.append(index)
        for index in to_be_removed_rows:
            field[1:index + 1, :] = field[0:index, :]
            field[0, :] = np.zeros(shape=(1, self.FIELD_WIDTH))
            remove_block = []
            for block in blocks:
                shape = block.get_shape()
                to_be_removed_shape = []
                anchor = block.get_anchor()

                for i, [x, y] in enumerate(shape):
                    if anchor[0] + x < index:
                        shape[i][0] += 1
                    elif anchor[0] + x == index:
                        to_be_removed_shape.append([x, y])

                if len(to_be_removed_shape) == len(shape):
                    remove_block.append(block)
                else:
                    for s in to_be_removed_shape:
                        shape.remove(s)
                    block.set_shape(shape)
            for r in remove_block:
                blocks.remove(r)
        return field, blocks, active_block

    def update_field(self, blocks, active_block):
        field = np.zeros(shape=(self.FIELD_HEIGHT, self.FIELD_WIDTH))
        x_active_anchor, y_active_anchor = active_block.get_anchor()
        for x, y in active_block.get_shape():
            field[x_active_anchor + x, y_active_anchor + y] = 1
        for block in blocks:
            anchor_x, anchor_y = block.get_anchor()
            for x, y in block.get_shape():
                field[anchor_x + x, anchor_y + y] = 1
        return field