from display import Display
from random_agent import RandomAgent
from game_manager import GameManager

if __name__ == '__main__':
    gm = GameManager()
    score = gm.start_game(RandomAgent(), display = False)
    print("Score:", score)
