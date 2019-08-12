import os
import sys
import collections as co
import numpy as np
import random
import pygame
from pygame import time
from pygame.color import THECOLORS

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.design import createDesignValues, samplePosition
from src.experiment import Experiment
from src.trial import ChaseTrial, CheckHumanResponse
from src.visualization import InitializeScreen, DrawState, DrawImage, DrawBackGround, DrawImageClick, DrawText, DrawFixationPoint, DrawStateWithRope
from src.pandasWriter import WriteDataFrameToCSV
from src.loadChaseData import GenerateTrajetoryData


def main():
    screenWidth = 800
    screenHeight = 800
    FPS = 60
    fullScreen = False
    initializeScreen = InitializeScreen(screenWidth, screenHeight, fullScreen)
    screen = initializeScreen()

    saveImage = False
    saveImageFile = 'noRopeCondition1'

    numOfAgent = 4
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
    colorSpace = [THECOLORS['grey'], THECOLORS['red'], THECOLORS['blue'], THECOLORS['yellow'], THECOLORS['purple'], THECOLORS['orange']]
    random.shuffle(colorSpace)
    # circleColorList = [THECOLORS['grey']] * numOfAgent
    # circleColorList = [THECOLORS['red'], THECOLORS['green'], THECOLORS['grey'], THECOLORS['yellow']]
    circleColorList = colorSpace[:numOfAgent]

    stateIndex = ['wolf', 'sheep', 'master', 'distractor']
    identityColorPairs = dict(zip(stateIndex, circleColorList))

    picturePath = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'pictures')
    resultsPath = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'results')


    introductionImage = pygame.image.load(os.path.join(picturePath, 'introduction2.png'))
    finishImage = pygame.image.load(os.path.join(picturePath, 'over.jpg'))
    introductionImage = pygame.transform.scale(introductionImage, (screenWidth, screenHeight))
    finishImage = pygame.transform.scale(finishImage, (int(screenWidth * 2 / 3), int(screenHeight / 4)))
    clickWolfImage = pygame.image.load(os.path.join(picturePath, 'clickwolf.png'))
    clickSheepImage = pygame.image.load(os.path.join(picturePath, 'clicksheep.png'))
    restImage = pygame.image.load(os.path.join(picturePath, 'rest.jpg'))
    # restImage = pygame.transform.scale(restImage, (screenWidth, screenHeight))

    drawImage = DrawImage(screen)
    drawText = DrawText(screen, fontSize, textColor)
    drawBackGround = DrawBackGround(screen, screenColor, xBoundary, yBoundary, lineColor, lineWidth)
    drawFixationPoint = DrawFixationPoint(screen, drawBackGround, fixationPointColor)
    drawImageClick = DrawImageClick(screen, clickImageHeight, drawText)
    drawState = DrawState(drawBackGround, numOfAgent, screen, circleSize)
    drawStateWithRope = DrawStateWithRope(drawBackGround, numOfAgent, screen, circleSize, ropeColor)

    conditionList = [1]#[1, 2, 3, 4]
    trajetoryIndexList =[1]# [1, 2, 3, 4, 5]
    dataFileDir = '../PataData'
    dataSetBoundary = [26, 26]
    generateTrajetoryData = GenerateTrajetoryData(dataFileDir, stimulusXBoundary, stimulusYBoundary, dataSetBoundary)
    stimulus = {condition: generateTrajetoryData(condition, trajetoryIndexList) for condition in conditionList}

    experimentValues = co.OrderedDict()

    # experimentValues["name"] = input("Please enter your name:").capitalize()
    experimentValues["name"] = 'csz'

    writerPath = os.path.join(resultsPath, experimentValues["name"]) + '.csv'
    writer = WriteDataFrameToCSV(writerPath)

    displayFrames = FPS * 3
    keysForCheck = {'f': 0, 'j': 1}
    checkHumanResponse = CheckHumanResponse(keysForCheck)
    trial = ChaseTrial(displayFrames, drawState, drawImage, stimulus, checkHumanResponse, colorSpace, numOfAgent, drawFixationPoint, drawText, drawImageClick, clickWolfImage, clickSheepImage, FPS, saveImage, saveImageFile)

    experiment = Experiment(trial, writer, experimentValues,drawImage,restImage)
    numOfBlock = 2
    numOfTrialsPerBlock = 1
    designValues = createDesignValues(conditionList * numOfTrialsPerBlock, numOfBlock)
    print(designValues)
    drawImage(introductionImage)
    experiment(designValues,numOfTrialsPerBlock)
    # drawImage(finishImage)
    print("Result saved at {}".format(writerPath))


if __name__ == '__main__':
    main()
