import numpy as np


class Updater:
    def __init__(self):
        self.data = np.zeros((104))
        self.pointer = 0
        self.samples = 1000

    def sample(self):
        return(self.data)
    def update(self,data):
        self.data = data
    def reset(self):
        pass
    