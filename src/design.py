import random
import numpy as np


def createDesignValues(condition, numOfBlock):
    designValues = list()
    for block in range(numOfBlock):
        random.shuffle(condition)
        designValues.append(condition)
    designValues = np.array(designValues).flatten().tolist()
    return designValues


def samplePosition(xBoundary, yBoundary):
    positionX = np.random.uniform(xBoundary[0], xBoundary[1])
    positionY = np.random.uniform(yBoundary[0], yBoundary[1])
    position = [positionX, positionY]
    return position
