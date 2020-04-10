from display import Display
from game import Game
from game_enums import GameStates


class GameManager:

    def __init__(self):
        self.display = Display()

    def start_game(self, agent, display=True):
        game = Game(agent)
        game.add_block()
        if display:
            self.display.show(game)
        while game.game_state != GameStates.OVER:
            game.update()
            if display:
                self.display.show(game)
        return game.score

