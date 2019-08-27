from subprocess import Popen, PIPE
import os
import sys
import collections as co
import numpy as np
import random
import pygame
import json
from pygame import time
from pygame.color import THECOLORS
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.design import createDesignValues, samplePosition
from src.experiment import Experiment
from src.trial import ReportTrial,OpenReportTxt
from src.visualization import InitializeScreen, DrawStateWithRope, DrawImage, DrawBackGround, DrawImageClick, DrawText, DrawFixationPoint, DrawStateWithRope,DrawState
from src.pandasWriter import WriteDataFrameToCSV
from src.loadChaseData import GenerateTrajetoryData
def crateVariableProduct(variableDict):
    levelNames = list(variableDict.keys())
    levelValues = list(variableDict.values())
    modelIndex = pd.MultiIndex.from_product(levelValues, names=levelNames)
    productDictList=[]
    productDictList=[{levelName:str(modelIndex.get_level_values(levelName)[modelIndexNumber]) \
            for levelName in levelNames} for modelIndexNumber in range(len(modelIndex))]
    return productDictList
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

def main():
    numOfAgent = 4
    sheepId = 0
    wolfId = 1
    masterId = 2
    distractorId = 3

    experimentValues = co.OrderedDict()
    experimentValues["condition"] = input("Please enter your condition 1 or 2:").capitalize()
    experimentValues["name"] = input("Please enter your name:").capitalize()
    #experimentValues["name"] = 'test'

    manipulatedHyperVariables = co.OrderedDict()
    conditionList = [int(experimentValues["condition"])]
    manipulatedHyperVariables['ChaseConditon']=conditionList
    trajetoryIndexList =[0]
    manipulatedHyperVariables['TrajIndex'] =  trajetoryIndexList

    exprimentVarableList=crateVariableProduct(manipulatedHyperVariables)

    screenWidth = 800
    screenHeight = 800
    FPS = 60
    fullScreen = True  
    initializeScreen = InitializeScreen(screenWidth, screenHeight, fullScreen)
    screen = initializeScreen()
 
    leaveEdgeSpace = 200
    circleSize = 10
    clickImageHeight = 80
    lineWidth = 3
    fontSize = 50
    xBoundary = [leaveEdgeSpace, screenWidth - leaveEdgeSpace * 2]
    yBoundary = [leaveEdgeSpace, screenHeight - leaveEdgeSpace * 2]
    stimulusXBoundary = [xBoundary[0] + circleSize, xBoundary[1] - circleSize]
    stimulusYBoundary = [yBoundary[0] + circleSize, yBoundary[1] - circleSize]

    screenColor = THECOLORS['black']
    lineColor = THECOLORS['white']
    textColor = THECOLORS['white']
    fixationPointColor = THECOLORS['white']
    ropeColor = THECOLORS['white']
    # colorSpace = [THECOLORS['grey'], THECOLORS['red'], THECOLORS['blue'], THECOLORS['yellow'], THECOLORS['purple'], THECOLORS['orange']]
    # random.shuffle(colorSpace)
    colorSpace=[THECOLORS['purple'],THECOLORS['orange'],THECOLORS['red'], THECOLORS['blue']] # sheep wolf master distractor
    # circleColorList = [THECOLORS['grey']] * numOfAgent
    # circleColorList = [THECOLORS['red'], THECOLORS['green'], THECOLORS['grey'], THECOLORS['yellow']]
    circleColorList = colorSpace[:numOfAgent]

    picturePath = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'pictures')
    resultsPath = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'results')

    introductionImage1 = pygame.image.load(os.path.join(picturePath, 'report1.png'))
    finishImage = pygame.image.load(os.path.join(picturePath, 'over.jpg'))
    introductionImage1 = pygame.transform.scale(introductionImage1, (int(screenWidth*3/4), int(screenHeight/4)))
    finishImage = pygame.transform.scale(finishImage, (int(screenWidth * 2 / 3), int(screenHeight / 4)))
    restImage = pygame.image.load(os.path.join(picturePath, 'rest.jpg'))
    reportInstrucImage=pygame.image.load(os.path.join(picturePath, 'report2.png'))
    reportInstrucImage  = pygame.transform.scale(reportInstrucImage, (int(screenWidth*1.4*3/5), int(screenHeight*1.7*2/5)))
    drawImage = DrawImage(screen)
    drawText = DrawText(screen, fontSize, textColor)
    drawBackGround = DrawBackGround(screen, screenColor, xBoundary, yBoundary, lineColor, lineWidth)
    drawFixationPoint = DrawFixationPoint(screen, drawBackGround, fixationPointColor)
    drawImageClick = DrawImageClick(screen, clickImageHeight, drawText)

    positionIndex = [0, 1]
    drawState = DrawState(screen, circleSize, numOfAgent, positionIndex, drawBackGround)
    # drawStateWithRope = DrawStateWithRope(screen, circleSize, numOfAgent, positionIndex, ropeColor, drawBackground)    
   

    dataFileDir = '../PataData'
    rawXRange = [-10, 10]
    rawYRange = [-10, 10]
    scaledXRange = [200, 600]
    scaledYRange = [200, 600]
    scaleTrajectory = ScaleTrajectory(positionIndex, rawXRange, rawYRange, scaledXRange, scaledYRange)
    oldFPS = 5
    adjustFPS = AdjustDfFPStoTraj(oldFPS, FPS)
    getTrajectory = lambda trajectoryDf: scaleTrajectory(adjustFPS(trajectoryDf))
    trajectoryDf = lambda condition,index: pd.read_pickle(os.path.join(dataFileDir, 'condition={}'.format(condition)+'sampleIndex={}.pickle'.format(index)))
    stimulus = {condition:[getTrajectory(trajectoryDf(condition,index)) for index in trajetoryIndexList] for condition in conditionList}

    writerPath = os.path.join(resultsPath, experimentValues["name"]) + experimentValues["condition"]+'.csv'
    writer = WriteDataFrameToCSV(writerPath)

    txtPath=(os.path.join(resultsPath,experimentValues["condition"]+'-'+experimentValues["name"]+'.txt'))
    openReportTxt=OpenReportTxt(txtPath)
    displayFrames = 600

    trial =ReportTrial(conditionList,displayFrames, drawState, drawImage, stimulus, colorSpace, numOfAgent, drawFixationPoint, drawText,  FPS,reportInstrucImage,openReportTxt)
    experiment = Experiment(trial, writer, experimentValues,drawImage,restImage,drawBackGround,hasRest=False)
    numOfBlock = 1
    numOfTrialsPerBlock = 1
    designValues = createDesignValues(exprimentVarableList * numOfTrialsPerBlock, numOfBlock)
    
    restDuration=3
    drawImage(introductionImage1) 

    
    experiment(designValues,restDuration)
    # drawBackGround()
    # drawImage(finishImage)


    print("Result saved at {}".format(txtPath))



if __name__ == "__main__":
	main()



