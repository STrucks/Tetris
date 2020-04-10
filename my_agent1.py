from abstract_agent import AbstractAgent
import

class MyAgent1(AbstractAgent):

    def __init__(self):
        rl.agents.dqn.DQNAgent(model, policy=None, test_policy=None, enable_double_dqn=True,
                               enable_dueling_network=False, dueling_type='avg')

    def move(self, field, inactive_blocks, active_block):
