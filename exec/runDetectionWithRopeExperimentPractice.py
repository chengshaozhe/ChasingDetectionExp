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
from src.design import createDesignValues, samplePosition,crateVariableProduct
from src.experiment import Experiment
from src.trial import ChaseTrialWithRope, CheckHumanResponse
from src.visualization import InitializeScreen, DrawImage, DrawBackGround, DrawImageClick, DrawText, DrawFixationPoint, DrawStateWithRope,DrawState
from src.pandasWriter import WriteDataFrameToCSV
from src.loadChaseData import GenerateTrajetoryData,ScaleTrajectory,AdjustDfFPStoTraj


def main():
    numOfAgent = 4
    sheepId = 0
    wolfId = 1
    masterId=2
    distractorId=3

    manipulatedHyperVariables = co.OrderedDict()
    conditionList = [1,2,3,4]  
                        #1：Chasing Present Master-Wolf Line; 2：Absent Master-Wolf Line 
                        #3：Chasing Present Master-Distractor Line; 4：Absent Master-Distractor Line 
    manipulatedHyperVariables['ChaseCondition']=conditionList
    trajetoryIndexList =[-1]
    manipulatedHyperVariables['TrajIndex'] =  trajetoryIndexList
    
    conditionValues = {1:[wolfId, masterId],2:[wolfId, masterId],3:[distractorId, masterId],4:[distractorId, masterId]}
    
    print('loading')
    positionIndex = [0, 1]
    FPS = 60
    dataFileDir = '../PataData/withLineRescale'
    rawXRange = [-10, 10]
    rawYRange = [-10, 10]
    scaledXRange = [200, 600]
    scaledYRange = [200, 600]
    scaleTrajectory = ScaleTrajectory(positionIndex, rawXRange, rawYRange, scaledXRange, scaledYRange)
    oldFPS = 5
    # adjustFPS = AdjustDfFPStoTraj(oldFPS, FPS)
    # getTrajectory = lambda trajectoryDf: scaleTrajectory(adjustFPS(trajectoryDf))
    trajectoryDf = lambda condition,index: pd.read_pickle(os.path.join(dataFileDir,'condition={}'.format(condition)+'_Index=({}).pickle'.format(index)))
    # stimulus = {condition:[getTrajectory(trajectoryDf(condition,index)) for index in trajetoryIndexList] for condition in conditionList}
    stimulus = {condition:{index:trajectoryDf(condition,index) for index in trajetoryIndexList} for condition in conditionList}
    print('loding success')

    experimentValues = co.OrderedDict()
    # experimentValues["name"] = input("Please enter your name:").capitalize()
    experimentValues["name"]='Practice'    
    screenWidth = 800
    screenHeight = 800

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

    screenColor = THECOLORS['black']
    lineColor = THECOLORS['white']
    textColor = THECOLORS['white']
    fixationPointColor = THECOLORS['white']

    colorSpace=[(203,164,4,255),(49,153,0,255),(255,90,16,255),(251,7,255,255),(9,204,172,255),(3,28,255,255)]

    picturePath = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'pictures')
    resultsPath = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'results')

    introductionImage1 = pygame.image.load(os.path.join(picturePath, 'withLineIntroduction1.png'))
    introductionImage2 = pygame.image.load(os.path.join(picturePath, 'introduction2.png'))
    finishImage = pygame.image.load(os.path.join(picturePath, 'over.jpg'))
    introductionImage1 = pygame.transform.scale(introductionImage1, (screenWidth, screenHeight))
    introductionImage2 = pygame.transform.scale(introductionImage2, (screenWidth, screenHeight))

    finishImage = pygame.transform.scale(finishImage, (int(screenWidth * 2 / 3), int(screenHeight / 4)))
    clickWolfImage = pygame.image.load(os.path.join(picturePath, 'clickwolf.png'))
    clickSheepImage = pygame.image.load(os.path.join(picturePath, 'clicksheep.png'))
    restImage = pygame.image.load(os.path.join(picturePath, 'rest.jpg'))

    drawImage = DrawImage(screen)
    drawText = DrawText(screen, fontSize, textColor)
    drawBackGround = DrawBackGround(screen, screenColor, xBoundary, yBoundary, lineColor, lineWidth)
    drawFixationPoint = DrawFixationPoint(screen, drawBackGround, fixationPointColor)
    drawImageClick = DrawImageClick(screen, clickImageHeight, drawText)
   
    ropeColor = THECOLORS['grey']
    ropeWidth = 4
    numRopePart = 9
    ropePartIndex = list(range(numOfAgent, numOfAgent + numRopePart))
    drawStateWithRope = DrawStateWithRope(screen, circleSize, numOfAgent, positionIndex, ropePartIndex, ropeColor, ropeWidth, drawBackGround)

    writerPath = os.path.join(resultsPath, experimentValues["name"]) + '.csv'
    writer = WriteDataFrameToCSV(writerPath)

    displayFrames = FPS*20
    keysForCheck = {'f': 0, 'j': 1}
    checkHumanResponse = CheckHumanResponse(keysForCheck)
    #trial = ChaseTrial(conditionList,displayFrames, drawState, drawImage, stimulus, checkHumanResponse, colorSpace, numOfAgent, drawFixationPoint, drawText, drawImageClick, clickWolfImage, clickSheepImage, FPS)
    trial = ChaseTrialWithRope(conditionValues,displayFrames, drawStateWithRope, drawImage, stimulus, checkHumanResponse, colorSpace, numOfAgent, drawFixationPoint, drawText, drawImageClick, clickWolfImage, clickSheepImage, FPS)
    
    experiment = Experiment(triasl, writer, experimentValues,drawImage,restImage,drawBackGround)
    
    numOfBlock =1
    numOfTrialsPerBlock = 1
    exprimentVarableList=crateVariableProduct(manipulatedHyperVariables)
    designValues = createDesignValues(exprimentVarableList * numOfTrialsPerBlock, numOfBlock)
    
    drawImage(introductionImage1)
    drawImage(introductionImage2)
    
    restDuration=20
    experiment(designValues,restDuration)
    # self.darwBackground()
    drawImage(finishImage)


    print("Result saved at {}".format(writerPath))


if __name__ == '__main__':
    main()
