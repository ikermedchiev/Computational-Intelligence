import numpy as numpy
from numpy import random
import matplotlib.pyplot as plt

def sigmoid(x):
    """Return the sigmoid of the given x"""
    s = 1 / (1 + numpy.exp(-x))
    return s

class perceptron:
    def __init__(self):
        self.weights = random.rand(2)
        self.threshold = 0.5
        self.learningRate = 0.01
        pass

    def output(self, inputs):
        sum = 0.0
        for i, input in enumerate(inputs):
            weight = self.weights[i]
            sum += weight * input
        return sigmoid(sum - self.threshold)
        #if sum >= self.threshold:
        #    return 1
        #return 0

    def adjust(self, inputs, error):
        for i, input in enumerate(inputs):
            self.weights[i] = self.weights[i] + \
                (self.learningRate * input * error)


p = perceptron()
print(f"before: {p.weights}")
dataset_or = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]

dataset_and = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]

dataset_xor = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]

dataset = dataset_or
mse = 2
mses = []
#while mse > 1e-6:
for i in range(0, 1000):
    mse = 0.0
    for el in dataset:
        inputs = el[:2]
        expected = el[2]
        actual = p.output(inputs)
        error = expected - actual
        p.adjust(inputs, error)
        mse += (error * error)
    # get the mean error
    mse = mse / len(dataset)
    mses.append(mse)
    # print(mse)
plt.plot(mses)
plt.ylabel('Mean Standard Error')
plt.xlabel('Epoch')
plt.suptitle("MSE over Epoch")
print(f"after: {p.weights}")
plt.show()
# what is the error?
