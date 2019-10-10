import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pygame
from src.visualization import DrawState, DrawImage, DrawBackground, DrawImageClick, DrawText
from src.design import samplePosition
from src.trial import ChaseTrial, CheckHumanResponse
import random
from pygame.color import THECOLORS

if __name__ == '__main__':
    pygame.init()
    screenWidth = 1024
    screenHeight = 1024
    screen = pygame.display.set_mode((screenWidth, screenHeight))

    leaveEdgeSpace = 200
    circleSize = 10
    imageHeight = 80
    lineWidth = 1
    xBoundary = [leaveEdgeSpace, screenWidth - leaveEdgeSpace * 2]
    yBoundary = [leaveEdgeSpace, screenHeight - leaveEdgeSpace * 2]
    numOfAgent = 4

    screenColor = THECOLORS['black']
    circleColorList = [THECOLORS['grey']] * numOfAgent
    circleSize = 10
    lineColor = THECOLORS['white']
    textColor = THECOLORS['green']

    drawImage = DrawImage(screen, imageHeight)
    drawText = DrawText(screen)
    drawImageClick = DrawImageClick(screen, imageHeight, circleColorList, drawText)
    drawBackground = DrawBackground(screen, xBoundary, yBoundary, lineColor, lineWidth)
    drawState = DrawState(drawBackground, numOfAgent, screen, screenColor, circleColorList, circleSize)

    picturePath = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'pictures')

    keysForCheck = {'f': 0, 'j': 1}
    clickWolfImage = pygame.image.load(os.path.join(picturePath, 'clickwolf.png'))
    clickSheepImage = pygame.image.load(os.path.join(picturePath, 'clicksheep.png'))
    checkHumanResponse = CheckHumanResponse(keysForCheck, drawImageClick, clickWolfImage, clickSheepImage)
    displayFrames = 10

    stimulusXBoundary = [xBoundary[0] + circleSize, xBoundary[1] - circleSize]
    stimulusYBoundary = [yBoundary[0] + circleSize, yBoundary[1] - circleSize]
    sampleTrajectory = lambda numOfAgent, displayFrames: [[samplePosition(stimulusXBoundary, stimulusYBoundary) for i in range(numOfAgent)] for j in range(displayFrames)]

    stimulus = {1: sampleTrajectory(numOfAgent, displayFrames),
                2: sampleTrajectory(numOfAgent, displayFrames),
                3: sampleTrajectory(numOfAgent, displayFrames),
                4: sampleTrajectory(numOfAgent, displayFrames)}

    condition = [1, 2, 3, 4]
    trial = ChaseTrial(displayFrames, drawState, drawImage, stimulus, checkHumanResponse, clickWolfImage)
    randomCondition = random.choice(condition)
    results = trial(randomCondition)
    print(results)
