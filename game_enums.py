from enum import Enum


class GameStates(Enum):
    RUNNING = 0
    OVER = 1

class Actions(Enum):
    STAY = 0
    RIGHT = 1
    LEFT = 2
    ROTATE = 3

