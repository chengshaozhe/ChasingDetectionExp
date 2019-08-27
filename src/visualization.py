import pygame as pg
import numpy as np
import os


class InitializeScreen:
    def __init__(self, screenWidth, screenHeight, fullScreen):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.fullScreen = fullScreen

    def __call__(self):
        pg.init()
        if self.fullScreen:
            screen = pg.display.set_mode((self.screenWidth, self.screenHeight), pg.FULLSCREEN)
        else:
            screen = pg.display.set_mode((self.screenWidth, self.screenHeight))
        pg.display.init()
        pg.fastevent.init()
        return screen


class DrawBackGround():
    def __init__(self, screen, screenColor, xBoundary, yBoundary, lineColor, lineWidth):
        self.screen = screen
        self.screenColor = screenColor
        self.xBoundary = xBoundary
        self.yBoundary = yBoundary
        self.lineColor = lineColor
        self.lineWidth = lineWidth

    def __call__(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()
        self.screen.fill(self.screenColor)
        rectPos = [self.xBoundary[0], self.yBoundary[0], self.xBoundary[1], self.yBoundary[1]]
        pg.draw.rect(self.screen, self.lineColor, rectPos, self.lineWidth)
        return


class DrawFixationPoint():
    def __init__(self, screen, drawBackGround, fixationPointColor):
        self.screen = screen
        self.drawBackGround = drawBackGround
        self.screenCenter = [int(self.screen.get_width() / 2), int(self.screen.get_height() / 2)]
        self.fixationPointColor = fixationPointColor

    def __call__(self):
        self.drawBackGround()
        pg.draw.circle(self.screen, self.fixationPointColor, self.screenCenter, 5)
        pg.display.flip()
        pg.time.wait(2000)
        return


class DrawState:
    def __init__(self, screen, circleSize, numOfAgent, positionIndex, drawBackGround):
        self.screen = screen
        self.circleSize = circleSize
        self.numOfAgent = numOfAgent
        self.xIndex, self.yIndex = positionIndex
        self.drawBackGround = drawBackGround

    def __call__(self, state, circleColorList):
        self.drawBackGround()
        for agentIndex in range(self.numOfAgent):
            agentPos = [np.int(state[agentIndex][self.xIndex]), np.int(state[agentIndex][self.yIndex])]
            agentColor = circleColorList[agentIndex]
            pg.draw.circle(self.screen, agentColor, agentPos, self.circleSize)
        pg.display.flip()
        pg.time.wait(10)
        return self.screen

# class DrawState():
#     def __init__(self, drawBackGround, numOfAgent, screen, circleSize):
#         self.drawBackGround = drawBackGround
#         self.numOfAgent = numOfAgent
#         self.screen = screen
#         self.circleSize = circleSize

#     def __call__(self, state, circleColorList):
#         self.drawBackGround()
#         for i in range(self.numOfAgent):
#             agentPos = state[i]
#             pg.draw.circle(self.screen, circleColorList[i], [np.int(
#                 agentPos[0]), np.int(agentPos[1])], self.circleSize)

#         pg.display.flip()
#         pg.time.wait(10)
#         return self.screen


class DrawStateWithRope():
    def __init__(self, screen, circleSize, numOfAgent, positionIndex, ropePartIndex, ropeColor, ropeWidth, drawBackGround):
        self.screen = screen
        self.circleSize = circleSize
        self.numOfAgent = numOfAgent
        self.xIndex, self.yIndex = positionIndex
        self.ropePartIndex = ropePartIndex
        self.ropeColor = ropeColor
        self.ropeWidth = ropeWidth
        self.drawBackGround = drawBackGround

    def __call__(self, state, tiedAgentId, circleColorList):
        self.drawBackGround()

        if tiedAgentId:
            tiedAgentPos = [[np.int(state[agentId][self.xIndex]), np.int(state[agentId][self.yIndex])] for agentId in tiedAgentId]
            ropePosList = [[np.int(state[ropeId][self.xIndex]), np.int(state[ropeId][self.yIndex])] for ropeId in self.ropePartIndex]

            tiedPosList = [[ropePosList[i], ropePosList[i + 1]] for i in range(0, len(ropePosList) - 1)]
            tiedPosList.insert(0, [tiedAgentPos[0], ropePosList[0]])
            tiedPosList.insert(-1, [tiedAgentPos[1], ropePosList[-1]])

            [pg.draw.lines(self.screen, self.ropeColor, False, tiedPos, self.ropeWidth) for tiedPos in tiedPosList]

        for agentIndex in range(self.numOfAgent):
            agentPos = [np.int(state[agentIndex][self.xIndex]), np.int(state[agentIndex][self.yIndex])]
            agentColor = circleColorList[agentIndex]
            pg.draw.circle(self.screen, agentColor, agentPos, self.circleSize)
        pg.display.flip()
        pg.time.wait(10)

        return self.screen

# class DrawStateWithRope():
#     def __init__(self, screen, circleSize, numOfAgent, positionIndex, ropeColor, drawBackGround):
#         self.screen = screen
#         self.circleSize = circleSize
#         self.numOfAgent = numOfAgent
#         self.xIndex, self.yIndex = positionIndex
#         self.ropeColor = ropeColor
#         self.drawBackGround = drawBackGround

#     def __call__(self, state, tiedAgentId, circleColorList):
#         self.drawBackGround()
#         if tiedAgentId:
#             tiedAgentPos = [[np.int(state[agentId][self.xIndex]), np.int(state[agentId][self.yIndex])] for agentId in tiedAgentId]
#             pg.draw.lines(self.screen, self.ropeColor, False, tiedAgentPos, 3)

#         for agentIndex in range(self.numOfAgent):
#             agentPos = [np.int(state[agentIndex][self.xIndex]), np.int(state[agentIndex][self.yIndex])]
#             agentColor = circleColorList[agentIndex]
#             pg.draw.circle(self.screen, agentColor, agentPos, self.circleSize)
#         pg.display.flip()
#         pg.time.wait(10)

#         return self.screen
# class DrawStateWithRope():
#     def __init__(self, drawBackGround, numOfAgent, screen, circleSize, ropeColor):
#         self.drawBackGround = drawBackGround
#         self.numOfAgent = numOfAgent
#         self.screen = screen
#         self.circleSize = circleSize
#         self.ropeColor = ropeColor

#     def __call__(self, state, condition, circleColorList):
#         self.drawBackGround()
#         if condition == 1 or condition == 3:
#             pg.draw.lines(self.screen, self.ropeColor, False, [state[0], state[2]], 5)
#         if condition == 2 or condition == 4:
#             pg.draw.lines(self.screen, self.ropeColor, False, [state[0], state[3]], 5)
#         for i in range(self.numOfAgent):
#             agentPos = state[i]
#             pg.draw.circle(self.screen, circleColorList[i], [np.int(
#                 agentPos[0]), np.int(agentPos[1])], self.circleSize)
#             pg.display.flip()
#         pg.time.wait(10)

#         return self.screen


class DrawImage():
    def __init__(self, screen):
        self.screen = screen
        self.screenCenter = (self.screen.get_width() / 2, self.screen.get_height() / 2)

    def __call__(self, image):
        imageRect = image.get_rect()
        imageRect.center = self.screenCenter
        pause = True
        pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
        self.screen.blit(image, imageRect)
        pg.display.flip()
        while pause:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    pause = False
                elif event.type == pg.QUIT and event.key == pg.K_ESCAPE:
                    pg.quit()


class DrawImageClick():
    def __init__(self, screen, imageHeight, drawText):
        self.screen = screen
        self.imageHeight = imageHeight
        self.screenCenter = (self.screen.get_width() / 2, self.imageHeight)
        self.drawText = drawText

    def __call__(self, image, text, circleColorList):
        imageRect = image.get_rect()
        imageRect.center = self.screenCenter
        pause = True
        self.screen.blit(image, imageRect)
        screensurf = pg.display.get_surface()
        pg.display.flip()
        while pause:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    mousePos = pg.mouse.get_pos()
                    mousePixel = screensurf.get_at(mousePos)
                    if mousePixel in circleColorList:
                        self.drawText(text, mousePos)
                        chosenIndex = circleColorList.index(mousePixel)
                        pause = False
                elif event.type == pg.QUIT:
                    pg.quit()
        return chosenIndex


class DrawText():
    def __init__(self, screen, fontSize, textColor):
        self.screen = screen
        self.fontSize = fontSize
        self.textColor = textColor

    def __call__(self, text, textPosition):
        font = pg.font.Font(None, self.fontSize)
        textObj = font.render(text, 1, self.textColor)
        self.screen.blit(textObj, textPosition)
        pg.display.flip()
        return


if __name__ == "__main__":
    pg.init()
    screenWidth = 720
    screenHeight = 720
    screen = pg.display.set_mode((screenWidth, screenHeight))
    import os
    picturePath = os.path.abspath(os.path.join(
        os.getcwd(), os.pardir)) + '/pictures/'
    restImage = pg.image.load(picturePath + 'rest.png')
    drawImage = DrawImage(screen)
    introductionImage = pg.image.load(picturePath + 'introduction.png')
    introductionImage = pg.transform.scale(introductionImage, (screenWidth, screenHeight))
    drawImage(introductionImage)
    pg.quit()
