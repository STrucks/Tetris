import numpy as np
from config_loader import config

class Block:

    def __init__(self, spawn_point):
        self.FIELDWIDTH = config['FIELD-WIDTH']
        self.FIELDHEIGHT = config['FIELD-HEIGHT']
        p_shapes = self._possible_shapes()
        self.shape = p_shapes[np.random.randint(0, len(p_shapes))]
        #self.shape = p_shapes[-1]
        self.anchor = spawn_point
        self.WIDTH = np.max(self.shape, axis=0)[1] + 1
        self.HEIGHT = np.max(self.shape, axis=0)[0] + 1
        self.COLOR = self._get_color()

    def get_anchor(self):
        return self.anchor

    def get_shape(self):
        return self.shape

    def set_anchor(self, x, y):
        self.anchor = [x, y]

    def _possible_shapes(self):
        shapes = [
            [[0, 0], [0, 1], [0, 2], [0, 3]],
            [[0, 0], [0, 1], [1, 1], [1, 2]],
            [[0, 0], [1, 0], [1, 1], [2, 1]],
            [[0, 0], [0, 1], [1, 0], [1, 1]],
            [[0, 0], [0, 1], [0, 2], [1, 1]],
            [[0, 0], [0, 1], [0, 2], [1, 2]],
            [[0, 0], [0, 1], [0, 2], [1, 0]],
            [[0, 0], [1, 0]]
        ]
        return shapes

    def get_coords(self):
        coords = [[self.anchor[0] + x, self.anchor[1] + y] for [x, y] in self.shape]
        return coords

    def remove_coord(self, coord):
        x = self.anchor[0] - coord[0]
        y = self.anchor[1] - coord[1]
        self.shape.remove([x, y])

    def _get_color(self):
        pos_colors = ["red", "yellow", "green", "white", "grey", "magenta", "cyan"]
        return pos_colors[np.random.randint(0, len(pos_colors))]

    def set_shape(self, shape):
        self.shape = []
        for [x, y] in shape:
            self.shape.append([x, y])
        self.WIDTH = np.max(self.shape, axis=0)[1] + 1
        self.HEIGHT = np.max(self.shape, axis=0)[0] + 1

    def rotate(self):
        original = []
        for i in range(self.HEIGHT):
            row = []
            for j in range(self.WIDTH):
                if [i, j] in self.shape:
                    row.append(1)
                else:
                    row.append(0)
            original.append(row)
        rotated = list(zip(*original[::-1]))
        new_shape = []
        for x, row in enumerate(rotated):
            for y, value in enumerate(row):
                if value == 1:
                    new_shape.append([x, y])
        return new_shape

