import numpy as np

class DataProvider:
    def __init__(self, data):
      self.data = data
      self.samples = len(data)
      self.pointer = 0

    def sample(self):
      if self.pointer >= self.samples-1:
        self.pointer = 0
      else:
        self.pointer += 1
      sample = self.data.loc[self.pointer]
      return(np.array(sample,dtype = np.float32))

    def reset(self):
      self.pointer = np.random.randint(self.samples)