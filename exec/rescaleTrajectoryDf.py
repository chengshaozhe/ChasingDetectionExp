import os
import sys
import collections as co
import pickle
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.loadChaseData import GenerateTrajetoryData,ScaleTrajectory,AdjustDfFPStoTraj
def saveToPickle(data, path):
    pklFile = open(path, "wb")
    pickle.dump(data, pklFile)
    pklFile.close()
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
    dataFileDir = '../PataData/withLine'
    rawXRange = [-10, 10]
    rawYRange = [-10, 10]
    scaledXRange = [200, 600]
    scaledYRange = [200, 600]
    scaleTrajectory = ScaleTrajectory(positionIndex, rawXRange, rawYRange, scaledXRange, scaledYRange)
    oldFPS = 5
    adjustFPS = AdjustDfFPStoTraj(oldFPS, FPS)
    getTrajectory = lambda trajectoryDf: scaleTrajectory(adjustFPS(trajectoryDf))
    trajectoryDf = lambda condition,index: pd.read_pickle(os.path.join(dataFileDir, '{}'.format(condition)+' ({}).pickle'.format(index)))
    stimulus = {condition:{index:getTrajectory(trajectoryDf(condition,index)) for index in trajetoryIndexList} for condition in conditionList}
    
    savedataFileDir='../PataData/withLineRescale'
    [[saveToPickle(stimulus[condition][index],os.path.join(savedataFileDir,'condition={}'.format(condition)+'_Index=({}).pickle'.format(index))) for index in trajetoryIndexList]  for condition in conditionList]


    print('loding success')

if __name__ == '__main__':
    main()
