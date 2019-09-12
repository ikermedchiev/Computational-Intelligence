import csv
import constants
import numpy as np
from random import shuffle


def is_number(value):
    """Check if the given string is a number"""
    try:
        float(value)
        return True
    except ValueError:
        return False

def _import_csv(path):
    data = []
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for index, element in enumerate(row):
                if is_number(element):
                    row[index] = float(element)
            data.append(row)
    return data


def process_targets(targets_raw):
    for row in targets_raw:
        t = int(row[0])
        row[0] = 0
        for _ in range(1, 7):
            row.append(0)
        row[t-1] = 1
    return targets_raw
    
def split(dataset):
    return list([dataset[i::constants.split_count] for i in range(constants.split_count)])

def output_csv(output, outputpath):
    with open(outputpath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in output:
            writer.writerow(row)


def import_csvs():
    """import our csvs to use"""
    dataset:list(list) = _import_csv(constants.features_csv)
    targets_raw:list(list) = _import_csv(constants.targets_csv)
    unknown = _import_csv(constants.unknown_csv)
    process_targets(targets_raw)

    for index, element in enumerate(dataset):
        element.append(targets_raw[index])
    shuffle(dataset)
    
    # data_np = np.asarray(dataset)
    # split = np.array_split(dataset, constants.split_count, axis=0)
    return dataset, unknown
