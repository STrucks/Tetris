from game_manager import GameManager
from Agents.ga_agent import Individuum

class Trainer:
    """
    This class trains NN
    """

    def __init__(self):
        self.gm = GameManager()

        # fill best_agents with 10 new agents
        # the array is: [[agent, performance], ...]
        self.best_agents = [[Individuum(), 0] for i in range(10)]

    def train_next_generation(self):
        # let all agents perform:
        for agent, score in self.best_agents:
            score = self.gm.start_game(agent, display=False)
            print("Score:", score)
