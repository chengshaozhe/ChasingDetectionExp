import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import random
import numpy as np

def adjustPostionDF(df, xPosIndex, yPosIndex, stimulusXBoundary, stimulusYBoundary, dataSetBoundary):
    df[xPosIndex] = df[xPosIndex] * stimulusXBoundary[1] / dataSetBoundary[0] + stimulusXBoundary[0]
    df[yPosIndex] = df[yPosIndex] * stimulusYBoundary[1] / dataSetBoundary[1] + stimulusYBoundary[0]
    adjustPostionDF = df
    return adjustPostionDF
class ScaleTrajectory:
    def __init__(self, positionIndex, rawXRange, rawYRange, scaledXRange, scaledYRange):
        self.xIndex, self.yIndex = positionIndex
        self.rawXMin, self.rawXMax = rawXRange
        self.rawYMin, self.rawYMax = rawYRange

        self.scaledXMin, self.scaledXMax = scaledXRange
        self.scaledYMin, self.scaledYMax = scaledYRange

    def __call__(self, originalTraj):
        xScale = (self.scaledXMax - self.scaledXMin) / (self.rawXMax - self.rawXMin)
        yScale = (self.scaledYMax - self.scaledYMin) / (self.rawYMax - self.rawYMin)

        adjustX = lambda rawX: (rawX - self.rawXMin) * xScale + self.scaledXMin
        adjustY = lambda rawY: (rawY - self.rawYMin) * yScale + self.scaledYMin

        adjustPair = lambda pair: [adjustX(pair[0]), adjustY(pair[1])]
        agentCount = len(originalTraj[0])

        adjustState = lambda state: [adjustPair(state[agentIndex]) for agentIndex in range(agentCount)]
        trajectory = [adjustState(state) for state in originalTraj]

        return trajectory
class AdjustDfFPStoTraj:
    def __init__(self, oldFPS, newFPS):
        self.oldFPS = oldFPS
        self.newFPS = newFPS

    def __call__(self, trajDf):
        xValue = [value['xPos'] for key, value in trajDf.groupby('agentId')]
        yValue = [value['yPos'] for key, value in trajDf.groupby('agentId')]

        timeStepsNumber = len(xValue[0])
        adjustRatio = self.newFPS // (self.oldFPS - 1)

        insertPositionValue = lambda positionList: np.array(
            [np.linspace(positionList[index], positionList[index + 1], adjustRatio, endpoint=False)
             for index in range(timeStepsNumber - 1)]).flatten().tolist()
        newXValue = [insertPositionValue(agentXPos) for agentXPos in xValue]
        newYValue = [insertPositionValue(agentYPos) for agentYPos in yValue]

        agentNumber = len(xValue)
        newTimeStepsNumber = len(newXValue[0])
        getSingleState = lambda time: [(newXValue[agentIndex][time], newYValue[agentIndex][time]) for agentIndex in range(agentNumber)]
        newTraj = [getSingleState(time) for time in range(newTimeStepsNumber)]
        return newTraj




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
