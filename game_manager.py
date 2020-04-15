from display import Display
from game import Game
from game_enums import GameStates
from my_agent1 import MyAgent1
from random_agent import RandomAgent


class GameManager:

    def __init__(self, ai="random"):
        self.display = Display()
        if ai == "random":
            self.agent = RandomAgent()
        elif ai == "my1":
            self.agent = MyAgent1()
        else:
            self.agent = RandomAgent()

    def start_game(self, display=True):
        game = Game(self.agent)
        game.add_block()
        if display:
            self.display.show(game)
        while game.game_state != GameStates.OVER:
            game.update()
            if display:
                self.display.show(game)
        return game.score

