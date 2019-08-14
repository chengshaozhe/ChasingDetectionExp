import numpy as np
import random
import collections as co
import pygame as pg
from pygame import time
from pygame.color import THECOLORS
import os
import sys
from subprocess import Popen, PIPE
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
class OpenReportTxt(object):
    def __init__(self, txtPath):
        self.txtPath=txtPath
        if  not os.path.exists(txtPath):
            txt=open(txtPath,'w')
            txt.close()            
    def __call__(self):   
        proc=Popen(['NOTEPAD',self.txtPath])
        proc.wait()

class CheckHumanResponse():
    def __init__(self, keysForCheck):
        self.keysForCheck = keysForCheck

    def __call__(self, initialTime, results, pause, circleColorList):
        for event in pg.fastevent.get():
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


class ChaseTrial():
    def __init__(self, condtionList,displayFrames, drawState, drawImage, stimulus, checkHumanResponse, colorSpace, numOfAgent, drawFixationPoint, drawText, drawImageClick, clickWolfImage, clickSheepImage, fps, saveImage, saveImageFile):
        self.displayFrames = displayFrames
        self.stimulus = stimulus
        self.drawState = drawState
        self.drawImage = drawImage
        self.checkHumanResponse = checkHumanResponse
        self.colorSpace = colorSpace
        self.numOfAgent = numOfAgent
        self.drawFixationPoint = drawFixationPoint
        self.drawText = drawText
        self.drawImageClick = drawImageClick
        self.clickWolfImage = clickWolfImage
        self.clickSheepImage = clickSheepImage
        self.fps = fps
        self.saveImage = saveImage
        self.saveImageFile = saveImageFile
        self.conditionList=condtionList

    def __call__(self, condition):
        results = co.OrderedDict()
        results["trail"] = ''
        results['condition'] = condition['ChaseConditon']
        results['trajetoryIndex']=condition['TrajIndex']
        results['response'] = ''
        results['reactionTime'] = ''
        results['chosenWolfIndex'] = ''
        results['chosenSheepIndex'] = ''
        print('1',condition,'2')

        trajetoryData = self.stimulus[int(condition['ChaseConditon'])][int(condition['TrajIndex'])]
        random.shuffle(self.colorSpace)
        circleColorList = self.colorSpace[:self.numOfAgent]

        pause = True
        initialTime = time.get_ticks()
        fpsClock = pg.time.Clock()
        while pause:
            pg.mouse.set_visible(False)
            self.drawFixationPoint()
            for t in range(self.displayFrames):
                state = trajetoryData[t]
                fpsClock.tick(self.fps)

                screen = self.drawState(state, circleColorList)
                # screen = self.drawState(state, condition, circleColorList)
                # screen = self.drawStateWithRope(state, condition, self.colorSpace)
                if self.saveImage == True:
                    currentDir = os.getcwd()
                    parentDir = os.path.abspath(os.path.join(currentDir, os.pardir))
                    saveImageDir = os.path.join(os.path.join(parentDir, 'data'), self.saveImageFile)
                    if not os.path.exists(saveImageDir):
                        os.makedirs(saveImageDir)
                    pg.image.save(screen, saveImageDir + '/' + format(t, '04') + ".png")

                results, pause = self.checkHumanResponse(initialTime, results, pause, circleColorList)
                if not pause:
                    break 

                if t == self.displayFrames - 1:
                    self.drawText('Please Response Now!', (screen.get_width() / 4, screen.get_height() / 1.2))
                    while pause:
                        results, pause = self.checkHumanResponse(initialTime, results, pause, circleColorList)
               

            if results['response'] == 1:
                pg.mouse.set_visible(True)
                chosenWolfIndex = self.drawImageClick(self.clickWolfImage, "W", circleColorList)
                chosenSheepIndex = self.drawImageClick(self.clickSheepImage, 'S', circleColorList)
                results['chosenWolfIndex'] = chosenWolfIndex
                results['chosenSheepIndex'] = chosenSheepIndex
                pg.time.wait(500)

        return results

class ReportTrial():
    def __init__(self, conditionList,displayFrames, drawState, drawImage, stimulus, colorSpace, numOfAgent, drawFixationPoint, drawText,  fps,reportInstrucImage,openReportTxt):
        self.conditionList=conditionList
        self.displayFrames = displayFrames
        self.stimulus = stimulus
        self.drawState = drawState
        self.drawImage = drawImage
        self.colorSpace = colorSpace
        self.numOfAgent = numOfAgent
        self.drawFixationPoint = drawFixationPoint
        self.drawText = drawText   
        self.fps = fps
        self.reportInstrucImage=reportInstrucImage
        self.openReportTxt=openReportTxt        
    def __call__(self, condition):
        results = co.OrderedDict()
        results["trail"] = ''
        results['condition'] = condition['ChaseConditon']
        results['trajetoryIndex']=condition['TrajIndex']
        trajetoryData = self.stimulus[int(condition['ChaseConditon'])][int(condition['TrajIndex'])]
        random.shuffle(self.colorSpace)
        circleColorList = self.colorSpace[:self.numOfAgent]

        pause = True
        initialTime = time.get_ticks()
        fpsClock = pg.time.Clock()
        pg.mouse.set_visible(False)
        self.drawFixationPoint()
        for t in range(self.displayFrames):
            state = trajetoryData[t]
            fpsClock.tick(self.fps)

            screen = self.drawState(state, circleColorList)
            # screen = self.drawState(state, condition, circleColorList)
            # screen = self.drawStateWithRope(state, condition, self.colorSpace)

        self.drawImage(self.reportInstrucImage)
        pg.quit()
        self.openReportTxt()
        # self.drawImage(self.reportInstrucImage)
        return results

if __name__ == "__main__":
    resultsPath = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'results')
    txtPath=(os.path.join(resultsPath,'k'+'.txt'))
    openReportTxt=OpenReportTxt(txtPath)
    openReportTxt()
