from game_manager import GameManager
from trainer import Trainer
from Agents.random_agent import RandomAgent
import pickle


def start_example_game():
    gm = GameManager()
    score = gm.start_game(RandomAgent(), display=True)
    print("Score:", score)


def start_ga_training():
    trainer = Trainer()
    iters = 100
    for i in range(iters):
        trainer.train_next_generation()
    trainer.export_best("best_agent_%d.pkl" % iters)


def start_with_existing_ga_agent():
    agent_src = "Training Output/best_agent_100.pkl"
    with open(agent_src, 'rb') as input:
        agent = pickle.load(input)
    gm = GameManager()
    score = gm.start_game(agent, display=True)
    print("Score:", score)

if __name__ == '__main__':
    #start_ga_training()
    start_with_existing_ga_agent()