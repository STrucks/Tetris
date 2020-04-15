from display import Display
from random_agent import RandomAgent
from my_agent1 import MyAgent1
from game_manager import GameManager

if __name__ == '__main__':
    gm = GameManager(ai="my1")
    score = gm.start_game(display=True)
    print("Score:", score)
