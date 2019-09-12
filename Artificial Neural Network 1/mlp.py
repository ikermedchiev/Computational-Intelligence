import numpy as np
from numpy import random
import copy
import constants


def sigmoid(x):
    """Return the sigmoid of the given x"""
    s = 1 / (1 + np.exp(-x))
    return s


class perceptron:
    def __init__(self, inputcount):
        self.weights = random.randn(inputcount)
        self.deltas = np.zeros((inputcount, constants.batchsize))
        # print(np.shape(self.deltas))
        self.errors = np.zeros(inputcount)
        self.best = np.zeros(inputcount)
        pass

    def output(self, inputs):
        x = 0.0
        for i, input in enumerate(inputs):
            weight = self.weights[i]
            x += weight * input
        x -= constants.threshold
        y = sigmoid(x)
        return y

    def addweight(self, delta, indexin, batchindex):
        self.deltas[indexin, batchindex] = delta

    def trainonline(self, delta, index):
        self.weights[index] += delta

    def savecurrent(self):
        """Saves these weigths as the current best weigths for this node"""
        self.best = np.copy(self.weights)

    def resetbest(self):
        self.weights = np.copy(self.best)

    def completebatch(self):
        """
        Called after completing a batch to calculate the averages and
        move into the correct direction.
        """
        averages = np.average(self.deltas, axis=1)
        for index, average in enumerate(averages):
            self.weights[index] += average
        pass

    def savestring(self):
        return str(self.weights)

    def __str__(self):
        return f"perceptron<w:{len(self.weights)}, d:{np.shape(self.deltas)}>"

    def __repr__(self):
        return self.__str__()


class MLP:
    def __init__(self, inputcount, hiddenlayercounts, outputcount):
        # first layer receives the inputs
        self.hiddenlayers = [[perceptron(inputcount)
                              for _ in range(0, hiddenlayercounts[0])]]

        # next the other hidden layers have as much as their previous ones

        for index in range(1, len(hiddenlayercounts)):
            layerinputcount = hiddenlayercounts[index - 1]
            layercount = hiddenlayercounts[index]
            self.hiddenlayers.append(
                [perceptron(layerinputcount) for _ in range(0, layercount)])

        # output has as many inputs as the last hidden layer has neurons
        self.outputlayer = [perceptron(hiddenlayercounts[-1])
                            for _ in range(0, outputcount)]

    def output(self, inputs):
        self.actual = [inputs]  # reset the self.actual

        for layer in self.hiddenlayers:
            outs = []
            ins = self.actual[-1]  # most recent output
            for percept in layer:
                res = percept.output(ins)
                outs.append(res)
            self.actual.append(outs)
        lastins = self.actual[len(self.actual) - 1]
        lastouts = []
        for percept in self.outputlayer:
            lastouts.append(percept.output(lastins))
        self.actual.append(lastouts)
        return lastouts

    def trainonline(self, ins, expected):
        self.output(ins)
        finaloutputdata = self.actual[-1]
        outerrors = [expected - out for out,
                     expected in zip(finaloutputdata, expected)]
        mse = sum(error * error for error in outerrors) / len(outerrors)
        outgradients = [out * (1 - out) * error for out,
                        error in zip(finaloutputdata, outerrors)]
        # print(f"Outputs: {finaloutputdata}\nErrors: {errors}\nGradients:{gradients}")
        for gradient, perceptron in zip(outgradients, self.outputlayer):
            for layerindex, prevout in enumerate(self.actual[-2]):
                # for every previous output
                deltaweight = constants.learningrate * prevout * gradient
                perceptron.trainonline(deltaweight, layerindex)
        preverrors = outerrors
        for layerindex in range(len(self.hiddenlayers) - 1, 0, -1):
            preverrors = self.calcLayerOnline(preverrors, layerindex)

        return mse

    def calcLayerOnline(self, preverrors, layerindex):
        """
        process the layer of the given index and output the errors you got
        """
        curerrors = []  # result array
        # this is the layer you are currently doing
        layer = self.hiddenlayers[layerindex]
        # layerabove could be the outputlayer
        if layerindex == len(self.hiddenlayers) - 1:
            layerabove = self.outputlayer
        else:
            layerabove = self.hiddenlayers[layerindex + 1]
        # inputs are the outputs of the layer before us (actual also contains inputs)
        # which is why we don't have to subtract
        layerinputs = self.actual[layerindex]
        # your own outputs
        myoutputs = self.actual[layerindex + 1]
        for pindex, perceptron in enumerate(layer):
            errorsum = sum(outtron.weights[pindex] * preverrors[outindex]
                           for outindex, outtron in enumerate(layerabove))
            errorgradient = myoutputs[pindex] * \
                (1 - myoutputs[pindex]) * errorsum
            for inputindex, inputvalue in enumerate(layerinputs):
                delta = constants.learningrate * errorgradient * inputvalue
                perceptron.trainonline(delta, layerindex)
            curerrors.append(errorgradient)
        return curerrors

    def train(self, ins, expected, batchindex):
        self.output(ins)
        # now self.actual is populated with the perceptron outputs
        finaloutputdata = self.actual[-1]
        outerrors = [expected - out for out,
                     expected in zip(finaloutputdata, expected)]
        mse = sum(error * error for error in outerrors) / len(outerrors)
        outgradients = [out * (1 - out) * error for out,
                        error in zip(finaloutputdata, outerrors)]
        # print(f"Outputs: {finaloutputdata}\nErrors: {errors}\nGradients:{gradients}")
        for gradient, perceptron in zip(outgradients, self.outputlayer):
            for layerindex, prevout in enumerate(self.actual[-2]):
                # for every previous output
                deltaweight = constants.learningrate * prevout * gradient
                perceptron.addweight(deltaweight, layerindex, batchindex)

        preverrors = outerrors
        for layerindex in range(len(self.hiddenlayers) - 1, 0, -1):
            preverrors = self.calcLayer(preverrors, batchindex, layerindex)

        return mse

    def calcLayer(self, preverrors, batchindex, layerindex):
        """
        process the layer of the given index and output the errors you got
        """
        curerrors = []  # result array
        # this is the layer you are currently doing
        layer = self.hiddenlayers[layerindex]
        # layerabove could be the outputlayer
        if layerindex == len(self.hiddenlayers) - 1:
            layerabove = self.outputlayer
        else:
            layerabove = self.hiddenlayers[layerindex + 1]
        # inputs are the outputs of the layer before us (actual also contains inputs)
        # which is why we don't have to subtract
        layerinputs = self.actual[layerindex]
        # your own outputs
        myoutputs = self.actual[layerindex + 1]
        for pindex, perceptron in enumerate(layer):
            errorsum = sum(outtron.weights[pindex] * preverrors[outindex]
                           for outindex, outtron in enumerate(layerabove))
            errorgradient = myoutputs[pindex] * \
                (1 - myoutputs[pindex]) * errorsum
            for inputindex, inputvalue in enumerate(layerinputs):
                delta = constants.learningrate * errorgradient * inputvalue
                perceptron.addweight(delta, inputindex, batchindex)
            curerrors.append(errorgradient)
        return curerrors

    def completebatch(self):
        for perceptron in self.outputlayer:
            perceptron.completebatch()
        for hiddenlayer in self.hiddenlayers:
            for perceptron in hiddenlayer:
                perceptron.completebatch()

    def savebest(self):
        # save the current state as the best state
        for perceptron in self.outputlayer:
            perceptron.savecurrent()
        for hiddenlayer in self.hiddenlayers:
            for perceptron in hiddenlayer:
                perceptron.savecurrent()

    def resetbest(self):
        for perceptron in self.outputlayer:
            perceptron.resetbest()
        for hiddenlayer in self.hiddenlayers:
            for perceptron in hiddenlayer:
                perceptron.resetbest()

    def currentmse(self, ins, expected):
        self.output(ins)
        # now self.actual is populated with the perceptron outputs
        finaloutputdata = self.actual[-1]
        errors = [expected - out for out,
                  expected in zip(finaloutputdata, expected)]
        mse = sum(error * error for error in errors) / len(errors)
        return mse

    def savenetwork(self, outputpath, correctness, validationcorrectness, validationmse, testmse):

        with open(outputpath, 'w', newline='') as file:

            file.write(f"""Test Correctness = {correctness}%
Test MSE: {testmse}
Validation MSE: {validationmse}
Validation Correctness: {validationcorrectness}
Constants:
hiddenlayers = {constants.hiddenlayers}
split count = {constants.split_count}
learningrate = {constants.learningrate}
threshold = {constants.threshold}
halftime = {constants.learningratehalftime}
respliteverynepochs = {constants.batchsize}
increasinglimit = {constants.increasinglimit}            
""")
            file.write("Output layer\n")
            for perceptron in self.outputlayer:
                file.write(perceptron.savestring() + "\n")
            for index, layer in enumerate(self.hiddenlayers):
                file.write(f"Hidden layer #{index}\n")
                for perceptron in layer:
                    file.write(perceptron.savestring() + "\n")


def maxonly(arr):
    """
    Only the maximum of this array is set to 1, else 0
    (if two numbers are equal both are set to 1)
    """
    mymax = max(arr)
    return [1 if el == mymax else 0 for el in arr]
