import numpy as np
import random
import collections as co
import pygame as pg
from pygame import time
from pygame.color import THECOLORS


class CheckHumanResponse():
    def __init__(self, keysForCheck):
        self.keysForCheck = keysForCheck

    def __call__(self, initialTime, results, pause, circleColorList):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    reactionTime = time.get_ticks() - initialTime
                    results['response'] = self.keysForCheck['f']
                    results['reactionTime'] = str(reactionTime)
                    pause = False

                if event.key == pg.K_j:
                    reactionTime = time.get_ticks() - initialTime
                    results['response'] = self.keysForCheck['j']
                    results['reactionTime'] = str(reactionTime)
                    pause = False

        pg.display.update()
        return results, pause


class PressToContinue():
    def __init__(self, allowedKey):
        self.allowedKey = allowedKeyList

    def __call__(self):
        pause = True
        pg.event.set_allowed(allowedKeyList)
        while pause:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    pause = False
                elif event.type == pg.QUIT:
                    pg.quit()


class ChaseTrial():
    def __init__(self, displayFrames, drawState, drawImage, stimulus, checkHumanResponse, colorSpace, numOfAgent, drawFixationPoint, drawImageClick, clickWolfImage, clickSheepImage, fps):
        self.displayFrames = displayFrames
        self.stimulus = stimulus
        self.drawState = drawState
        self.drawImage = drawImage
        self.checkHumanResponse = checkHumanResponse
        self.colorSpace = colorSpace
        self.numOfAgent = numOfAgent
        self.drawFixationPoint = drawFixationPoint
        self.drawImageClick = drawImageClick
        self.clickWolfImage = clickWolfImage
        self.clickSheepImage = clickSheepImage
        self.fps = fps

    def __call__(self, condition):
        results = co.OrderedDict()
        results["trail"] = ''
        results['condition'] = condition
        results['response'] = ''
        results['reactionTime'] = ''
        results['chosenWolfIndex'] = ''
        results['chosenSheepIndex'] = ''

        trajetoryData = self.stimulus[condition]
        random.shuffle(self.colorSpace)
        circleColorList = self.colorSpace[:self.numOfAgent]

        pause = True
        initialTime = time.get_ticks()
        while pause:
            pg.mouse.set_visible(False)
            fpsClock = pg.time.Clock()
            self.drawFixationPoint()
            for t in range(self.displayFrames):
                state = trajetoryData[t]
                # self.drawState(state, circleColorList)
                self.drawState(state, condition, circleColorList)
                fpsClock.tick(self.fps)
                results, pause = self.checkHumanResponse(initialTime, results, pause, circleColorList)
                if not pause:
                    break
            if not results:
                results, pause = self.checkHumanResponse(initialTime, results, pause, circleColorList)

            if results['response'] == 1:
                pg.mouse.set_visible(True)
                chosenWolfIndex = self.drawImageClick(self.clickWolfImage, "W", circleColorList)
                chosenSheepIndex = self.drawImageClick(self.clickSheepImage, 'S', circleColorList)
                results['chosenWolfIndex'] = chosenWolfIndex
                results['chosenSheepIndex'] = chosenSheepIndex
                pg.time.wait(500)
        return results
