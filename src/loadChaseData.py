import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import random


def adjustPostionDF(df, xPosIndex, yPosIndex, stimulusXBoundary, stimulusYBoundary, dataSetBoundary):
    df[xPosIndex] = df[xPosIndex] * stimulusXBoundary[1] / dataSetBoundary[0] + stimulusXBoundary[0]
    df[yPosIndex] = df[yPosIndex] * stimulusYBoundary[1] / dataSetBoundary[1] + stimulusYBoundary[0]
    adjustPostionDF = df
    return adjustPostionDF


class GenerateTrajetoryData():
    def __init__(self, dataFileDir, stimulusXBoundary, stimulusYBoundary, dataSetBoundary):
        self.dataFileDir = dataFileDir
        self.stimulusXBoundary = stimulusXBoundary
        self.stimulusYBoundary = stimulusYBoundary
        self.dataSetBoundary = dataSetBoundary

    def __call__(self, condition, trajetoryIndexList):
        trajetoryIndex = random.choice(trajetoryIndexList)
        fileName = str(condition) + '(' + str(trajetoryIndex) + ')' + '.xls'
        filePath = os.path.join(self.dataFileDir, fileName)
        df = pd.read_excel(filePath, header=None)
        xPosIndex = list(range(0, 8, 2))
        yPosIndex = list(range(1, 8, 2))
        adjustedDF = adjustPostionDF(df, xPosIndex, yPosIndex, self.stimulusXBoundary, self.stimulusYBoundary, self.dataSetBoundary)
        trajetoryData = [[[row[0], row[1]], [row[2], row[3]], [row[4], row[5]], [row[6], row[7]]] for index, row in adjustedDF.iterrows()]
        return trajetoryData


if __name__ == '__main__':
    dataFileDir = '../PataData'
    screenWidth = 1024
    screenHeight = 1024
    leaveEdgeSpace = 200
    circleSize = 10
    xBoundary = [leaveEdgeSpace, screenWidth - leaveEdgeSpace * 2]
    yBoundary = [leaveEdgeSpace, screenHeight - leaveEdgeSpace * 2]
    stimulusXBoundary = [xBoundary[0] + circleSize, xBoundary[1] - circleSize]
    stimulusYBoundary = [yBoundary[0] + circleSize, yBoundary[1] - circleSize]
    dataSetBoundary = [25, 25]
    generateTrajetoryData = GenerateTrajetoryData(dataFileDir, stimulusXBoundary, stimulusYBoundary, dataSetBoundary)

    conditionList = [1, 2, 3, 4]
    trajetoryIndexList = [1, 2, 3, 4, 5]
    chaseData = {condition: generateTrajetoryData(condition, trajetoryIndexList) for condition in conditionList}
    # print(chaseData)
