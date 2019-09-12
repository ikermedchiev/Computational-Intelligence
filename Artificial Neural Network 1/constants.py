"""
DON'T MODIFY THESE
"""
# The path to the features csv
features_csv = "features.txt"
# The path tp the targets csv
targets_csv = "targets.txt"
# The path to the unknown csv
unknown_csv = "unknown.txt"
# The output path
outputfolder = "output"
# outputpath = "output/known"
# how many output neurons we should have
target_count = 7
# how many inputs we have
input_count = 10

"""
MODIFY THESE
"""
# k-fold: how many sets should we have
# (currently only the validation and test set are split out)
# so this determines what fraction of the total these should be
# make sure this a product of 2, 2, 7, 11, and 17 to let the list end without rests
split_count = 17
# How fast we learn from our errors
learningrate = 0.12644193548440671
# threshold is used by the perceptrons to subtract from in the sigma
threshold = 0.5 
# how much the learning rate should be adjusted by every 10 epochs
learningratehalftime = -1
# whether we should reshuffle and split the batches every n folds
# -1 for no splitting
respliteverynepochs = -1
# how large out batches should be
batchsize = 1
# what amount of neurons each hidden layer should contain
hiddenlayers = [30]
# maximum amount of epochs
maxepochs = 50
# how many times the MSE of the validation set can increase
# before we stop training to prevent overtraining
increasinglimit = 3
# MSE limit when you want to stop training
mselimit = 0.05


def printconstants():
    print(f"""Constants:
hiddenlayers = {hiddenlayers}
split count = {split_count}
learningrate = {learningrate}
threshold = {threshold}
adjustmentlearning rate = {learningratehalftime}
batchsize = {batchsize}
increasinglimit = {increasinglimit}""")