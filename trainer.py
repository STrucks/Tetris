from game_manager import GameManager
from Agents.ga_agent import Individuum
from operator import itemgetter
import numpy as np
import pickle


class Trainer:
    """
    This class trains NN
    """

    def __init__(self):
        self.gm = GameManager()

        # fill best_agents with 20 new agents
        # the array is: [[agent, performance], ...]
        self.best_agents = [{"agent": Individuum(), "score": 0} for i in range(20)]

    def train_next_generation(self):
        # set all scores back to 0:
        for agent in self.best_agents:
           agent['score'] = 0
        # let all agents perform 10 times:
        for i in range(10):
            for agent in self.best_agents:
                score = self.gm.start_game(agent['agent'], display=False)
                agent['score'] += score

        # select top 5 agents:
        self.best_agents = sorted(self.best_agents, key=itemgetter('score'))
        self.best_agents = self.best_agents[-5:]

        print("best Agent scores:")
        print(" ".join([str(agent['score']) for agent in self.best_agents]))

        # add 15 new agents with slightly permutated weights:
        new_agents = []
        for i in range(15):
            # choose an agent:
            agent = np.random.choice(self.best_agents)

            # clone that agent
            new_agent = agent['agent'].clone()

            permutation_matrix_1 = np.random.choice([0, 0.05, -0.05], size=new_agent.nn.w1.shape, p=[0.95, 0.025, 0.025])
            permutation_matrix_2 = np.random.choice([0, 0.05, -0.05], size=new_agent.nn.w2.shape, p=[0.95, 0.025, 0.025])

            new_w1 = np.clip(np.multiply(new_agent.nn.w1, permutation_matrix_1), -50, 50)
            new_w2 = np.clip(np.multiply(new_agent.nn.w2, permutation_matrix_2), -50, 50)

            new_agent.nn.set_weights(new_w1, new_w2)
            self.best_agents.append({"agent": new_agent, "score": 0})


    def export_best(self, filename):
        # select best agent:
        self.best_agents = sorted(self.best_agents, key=itemgetter('score'))
        best_agent = self.best_agents[-1]['agent']

        with open('Training Output/' + filename, 'wb') as output:
            pickle.dump(best_agent, output, pickle.HIGHEST_PROTOCOL)

