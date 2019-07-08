import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import collections as co
from pygame import time
import pygame
from src.visualization import DrawState
from src.wrappers import createDesignValues, samplePosition
from src.trial import Trial, CheckHumanResponse
import random
from ddt import ddt, data, unpack
import unittest


@ddt
class TestEnvNoPhysics(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screenWidth = 720
        self.screenHeight = 720
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.screen.fill((0, 0, 0))
        self.keysForCheck = {'f': 0, 'j': 1}
        pygame.time.wait(3000)

    @data((time.get_ticks(), {}, False, {'response': 0, 'reactionTime': 1000}, True), (time.get_ticks(), {}, False, {'response': 0, 'reactionTime': 3000}, True))
    @unpack
    def testCheckHumanResponse(self, initialTime, results, pause, groudTruthResults, groudTruthPause):
        checkHumanResponse = CheckHumanResponse(self.keysForCheck)
        returnedResults, returnedPause = checkHumanResponse(initialTime, results, pause)
        print(returnedResults, returnedPause)
        truthValue = returnedResults['response'] == groudTruthResults['response']
        self.assertTrue(truthValue)
        self.assertTrue(int(returnedResults['reactionTime']) > int(groudTruthResults['reactionTime']))
        self.assertEqual(returnedPause, groudTruthPause)


if __name__ == '__main__':
    unittest.main()
