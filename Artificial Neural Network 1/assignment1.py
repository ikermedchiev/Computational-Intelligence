import methods
import constants
import mlp
from numpy import random


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


class assignment:
    def __init__(self):
        # this is where we initialize our MLP
        self.mlp = mlp.MLP(constants.input_count,
                           constants.hiddenlayers, constants.target_count)
        self.dataset, self.unknown = methods.import_csvs()
        random.shuffle(self.dataset)
        gen2 = chunks(self.dataset, len(self.dataset) // constants.split_count)
        split_dataset = list(gen2)
        self.trainingset = list(
            [item for sublist in split_dataset[:len(split_dataset) - 3] for item in sublist])
        self.validationset = split_dataset[-2]
        self.testingset = split_dataset[-1]
        self.resplit()

    def resplit(self):
        """Splits the training set into batches of the wanted size after shuffling """
        random.shuffle(self.trainingset)
        self.batches = list(chunks(self.trainingset, constants.batchsize))

    def trainbatch(self, batch):
        mses = []
        for index, row in enumerate(batch):
            ins = row[:-1]
            expected = row[-1]
            mses.append(self.mlp.train(ins, expected, index))
        self.mlp.completebatch()
        return sum(mses)

    def trainonline(self):
        for row in self.trainingset:
            self.mlp.trainonline(row[:-1], row[-1])
    
    def train(self):
        """
        Trains the MLP till the MSE is less than the goal
        """
        mses = []
        mse = self.validate()
        mses.append(mse)
        epochs = 0
        increasingcount = 0
        # first output starting MSE
        print(f"MSE at start: {mse}\n----\nStarting training\n-----")
        if constants.batchsize == 1:
            print("doing online training")
        while mse > constants.mselimit and epochs < constants.maxepochs:
            epochs += 1
            # if constants.batchsize > 1:
            for batch in self.batches:
                self.trainbatch(batch)
            # else:
            #     self.trainonline()

            # readjust learning rate if so desired
            if constants.learningratehalftime > 0 and epochs % constants.learningratehalftime == 0:
                constants.learningrate /= 2
            # calculate the correctness again
            mse = self.validate()
            if mse > mses[-1] + (constants.learningrate / 10):
                increasingcount += 1
                if increasingcount > constants.increasinglimit:
                    print("MSE went up too much")
                    # reset to the best saved score
                    self.mlp.resetbest()
                    break
            else:
                if increasingcount > 0:
                    increasingcount = 0
                self.mlp.savebest()
            mses.append(mse)
            print(
                f"Epoch: {epochs}, MSE = {mse:.4f}")
            if constants.respliteverynepochs > 0 and epochs % constants.respliteverynepochs == 0:
                print("Re-ordering all the batches")
                self.resplit()
            if epochs % 20 == 0 and mse > 0.075 - (epochs / 1000):
                # unsucessful batch, no need to save
                print("Unsuccesful")
                break

        correctness = self.test()
        print(
            f"Done with training, currently {correctness}% correct over validation set after {epochs} epochs with final MSE of {mse}")
        return mses

    def validate(self):
        """
        Gets the mse of the validation set
        """
        msesum = 0.0
        for row in self.validationset:
            ins = row[:-1]
            expected = row[-1]
            finaloutputdata = self.mlp.output(ins)
            outerrors = [expected - out for out,
                         expected in zip(finaloutputdata, expected)]
            mse = sum(error * error for error in outerrors) / len(outerrors)
            msesum += mse
        msesum /= len(self.validationset)
        return msesum

    def validationCorrectness(self):
        errors = 0
        msesum = 0.0
        for row in self.validationset:
            ins = row[:-1]
            expected = row[-1]
            finaloutputdata = self.mlp.output(ins)
            outerrors = [expected - out for out,
                         expected in zip(finaloutputdata, expected)]
            mse = sum(error * error for error in outerrors) / len(outerrors)
            msesum += mse
            actual = mlp.maxonly(finaloutputdata)
            if expected != actual:
                # print(f"error found: {actual} != {expected}")
                errors += 1
        error_percentage = errors / len(self.validationset)
        validationmse = msesum / len(self.validationset)
        correctness = (1 - error_percentage) * 100
        # print(
        #     f"our algorithm is currently {correctness:.2f}% correct")
        return correctness, validationmse

    def final(self):
        """Outputs the results of parsing the unknowns to the output file """
        outputs = []
        for ins in self.unknown:
            actual = mlp.maxonly(self.mlp.output(ins))
            outputs.append([actual.index(max(actual)) + 1])
        return outputs

    def test(self):
        """
        we have to get the errors of the testing set after training
        so this is the validation
        """
        errors = 0
        msesum = 0.0
        for row in self.testingset:
            ins = row[:-1]
            expected = row[-1]
            finaloutputdata = self.mlp.output(ins)
            outerrors = [expected - out for out,
                         expected in zip(finaloutputdata, expected)]
            mse = sum(error * error for error in outerrors) / len(outerrors)
            msesum += mse
            actual = mlp.maxonly(finaloutputdata)
            if expected != actual:
                errors += 1
        error_percentage = errors / len(self.testingset)
        testmse = msesum / len(self.testingset)
        correctness = (1 - error_percentage) * 100
        return correctness, testmse

    def confusionmatrix(self):
        y_true = []
        y_pred = []
        for row in self.testingset:
            ins = row[:-1]
            expected = row[-1]
            actual = mlp.maxonly(self.mlp.output(ins))
            y_true.append(expected.index(max(expected))+1)
            y_pred.append(actual.index(max(actual))+1)
        confusion_matrix = ConfusionMatrix(y_true, y_pred)
        print("Confusion matrix:\n%s" % confusion_matrix)
        pass


def modifyvars():
    """
    Modifies the modifiable constants randomly
    """

    if random.randn() > 0:
        total = random.randint(7, 31)
        half = total // 2
        rest = total - half
        # modify the first hidden layer count
        constants.hiddenlayers[0] = half
        constants.hiddenlayers[1] = rest
    else:
        constants.hiddenlayers[0] = 10
        constants.hiddenlayers[1] = 10

    # set learning rate randomly
    constants.learningrate = random.uniform(0.0, 0.2)

    # batchsize
    if random.randn() > 0:
        constants.batchsize = random.randint(2, 300)
    else:
        constants.batchsize = 1

    # adjustment rate
    if random.randn() > 0:
        constants.learningratehalftime = random.randint(10, 100)
    else:
        constants.learningratehalftime = -1

    constants.printconstants()

    pass


graphing = False
confusion = True
plotting = True
if __name__ == "__main__":
     # execute if this file is run
    import os
    if not os.path.exists("output"):
        os.makedirs("output")
    if not os.path.exists("networks"):
        os.makedirs("networks")

    while not graphing:
        ass = assignment()
        epochs = len(ass.train())
        if epochs < 1:
            # modifyvars()
            continue
        correctness, testmse = ass.test() # % correct on test
        
        output = ass.final()
        validationcorrectness, validationmse = ass.validationCorrectness()
        
        ass.mlp.savenetwork(
            f"networks/network({epochs}_{validationmse}.txt", correctness, validationcorrectness, validationmse, testmse)
        methods.output_csv(
            output, f"{constants.outputfolder}/known_{validationmse}.txt")
        # modifyvars()

    if confusion:
        import matplotlib.pyplot as plt
        from pandas_ml import ConfusionMatrix
        ass = assignment()
        ass.train()
        ass.confusionmatrix()
    if plotting:
        import matplotlib.pyplot as plt
        ass = assignment()
        mses = ass.train()
        plt.plot(mses)
        plt.ylabel("MSE")
        plt.xlabel("Epoch")
        plt.title("Best MSE over epoch")
        plt.show()

