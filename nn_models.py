#from keras import Sequential
#from keras.layers import Dense
import numpy as np
from util import softmax


class KerasMLP:

    def __init__(self, in_nodes, out_nodes, layers=1):

        #self.model = Sequential()
        #self.model.add(Dense(32, input_shape=(in_nodes, )))
        #for l in range(layers):
        #    self.model.add(Dense(32))
        #self.model.add(Dense(out_nodes, activation='softmax'))
        pass


class GA_MLP:
    """
    This class contains the the 'AI' of the individuals of the genetic algorithm.
    It will always be a MLP with 1 hidden layer for now
    """

    def __init__(self, in_nodes, out_nodes):
        self.w1 = np.random.rand(in_nodes, 20)
        self.w2 = np.random.rand(20, out_nodes)

    def forward(self, in_activation):
        activation = np.matmul(in_activation, self.w1)
        activation = np.matmul(activation, self.w2)
        return softmax(activation)

    def set_weights(self, w1, w2):
        self.w1 = w1
        self.w2 = w2