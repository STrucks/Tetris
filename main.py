from game_manager import GameManager
from trainer import Trainer
from Agents.random_agent import RandomAgent

def start_example_game():
    gm = GameManager()
    score = gm.start_game(RandomAgent(), display=True)
    print("Score:", score)


def start_ga_training():
    trainer = Trainer()
    trainer.train_next_generation()


if __name__ == '__main__':
    start_ga_training()
