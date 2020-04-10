from game import Game
from termcolor import colored, cprint
from os import system
import time

class Display:

    def __init__(self):
        pass

    def show(self, game:Game):
        print("\n"*30)
        for x, row in enumerate(game.field):
            print("|", end="")
            for y, value in enumerate(row):
                if [x, y] in game.active_block.get_coords():
                    print(colored("0", 'blue', "on_blue"), end="")
                else:
                    hit_flag = False
                    hitting_block = None
                    for b in game.blocks:
                        if [x, y] in b.get_coords():
                            hit_flag = True
                            hitting_block = b
                    if hit_flag:
                        print(colored("0", hitting_block.COLOR, "on_"+hitting_block.COLOR), end="")
                    else:
                        print(" ", end="")
            print("|", end="")
            print("")
        for i in range(game.FIELD_WIDTH+2):
            print("-", end="")
        print()
        time.sleep(0.5)

