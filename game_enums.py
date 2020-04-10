from enum import Enum


class GameStates(Enum):
    RUNNING = 0
    OVER = 1

class Actions(Enum):
    RIGHT = 0
    LEFT = 1
    ROTATE = 2
    STAY = 3

