import numpy as np
from copy import deepcopy

from block import Block
from config_loader import config
from game_enums import Actions, GameStates
from abstract_agent import AbstractAgent

import logging


class Game:

    def __init__(self, agent:AbstractAgent):
        logging.basicConfig(level=logging.DEBUG)
        self.FIELD_WIDTH:int = config['FIELD-WIDTH']
        self.FIELD_HEIGHT:int = config['FIELD-HEIGHT']
        self.field = np.zeros(shape=(self.FIELD_HEIGHT, self.FIELD_WIDTH))
        self.spawn_point = [0, int(self.FIELD_WIDTH/2)]
        self.active_block:Block = None
        self.blocks = []
        self.game_state:GameStates = GameStates.RUNNING
        self.agent: AbstractAgent = agent
        self.score = 0

    def update(self):
        self.move()
        self.apply_physics()
        self.update_field()
        if self.game_state == GameStates.RUNNING:
            self.score += 1


    def apply_physics(self):
        x_anchor, y_anchor = self.active_block.get_anchor()
        # check if block hit the bottom:
        if x_anchor < self.FIELD_HEIGHT - self.active_block.HEIGHT:
            # check if active block would collide with another block
            collide_flag = False
            new_x_anchor = x_anchor + 1
            for [x, y] in self.active_block.get_shape():
                if collide_flag:
                    continue
                for b in self.blocks:
                    occupied_anchor_x, occupied_anchor_y = b.get_anchor()
                    occupied_coords = [[occupied_anchor_x + x_o, occupied_anchor_y + y_o] for x_o, y_o in b.get_shape()]
                    if [new_x_anchor + x, y_anchor + y] in occupied_coords:
                        self.blocks.append(self.active_block)
                        self.active_block = Block(self.spawn_point)
                        collide_flag = True
                        if x_anchor == self.spawn_point[0] and y_anchor == self.spawn_point[1]:
                            self.game_state = GameStates.OVER
            if not collide_flag:
                self.active_block.set_anchor(new_x_anchor, y_anchor)
            else:
                self.check_complete_row()
        else:
            self.blocks.append(self.active_block)
            self.check_complete_row()
            self.active_block = Block(self.spawn_point)

    def update_field(self):
        self.field = np.zeros(shape=(self.FIELD_HEIGHT, self.FIELD_WIDTH))
        x_active_anchor, y_active_anchor = self.active_block.get_anchor()
        for x, y in self.active_block.get_shape():
            self.field[x_active_anchor + x, y_active_anchor + y] = 1
        for block in self.blocks:
            anchor_x, anchor_y = block.get_anchor()
            for x, y in block.get_shape():
                self.field[anchor_x + x, anchor_y + y] = 1

    def add_block(self):
        self.active_block = Block(self.spawn_point)

    def move(self):
        # there is a 33/33/33 chance the active block will move left or right or stand still
        x_anchor, y_anchor = self.active_block.get_anchor()
        action = self.agent.move(self)
        logging.debug("Next action: " + action.name)
        if action == Actions.ROTATE:
            new_shape = self.active_block.rotate()
            # check if the new coords are out of bounds:
            new_coords = [[self.active_block.anchor[0] + x, self.active_block.anchor[1] + y] for [x, y] in new_shape]
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
                for block in self.blocks:
                    if [x, y] in block.get_coords():
                        collide_flag = True
            if not collide_flag:
                self.active_block.set_shape(new_shape)
                logging.debug("rotated block successfully")
        else:
            movement = self.__convert_action2move(action)
            new_y_anchor = y_anchor + movement
            # check boundaries:
            if 0 <= new_y_anchor <= self.FIELD_WIDTH - self.active_block.WIDTH:
                collide_flag = False
                for [x, y] in self.active_block.get_shape():
                    if collide_flag:
                        continue
                    for b in self.blocks:
                        occupied_coords = b.get_coords()
                        if [x_anchor + x, new_y_anchor + y] in occupied_coords:
                            collide_flag = True

                if not collide_flag:
                    self.active_block.set_anchor(x_anchor, new_y_anchor)
                    logging.debug("moved block successfully")
            else:
                pass

    def __convert_action2move(self, action:Actions):
        if action == Actions.RIGHT:
            return 1
        elif action == Actions.LEFT:
            return -1
        elif action == Actions.STAY:
            return 0
        else:
            return 0

    def check_complete_row(self):
        # check if there is a complete row:
        to_be_removed_rows = []
        self.update_field()
        for index, row in enumerate(self.field):
            if np.sum(row) == self.FIELD_WIDTH:
                to_be_removed_rows.append(index)
                self.score += 20
        for index in to_be_removed_rows:
            self.field[1:index + 1, :] = self.field[0:index, :]
            self.field[0, :] = np.zeros(shape=(1, self.FIELD_WIDTH))
            remove_block = []
            for block in self.blocks:
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
                self.blocks.remove(r)

    def get_score(self):
        return self.score

    def get_representations(self):
        return deepcopy(self.field), deepcopy(self.blocks), deepcopy(self.active_block)