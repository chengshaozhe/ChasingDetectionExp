
#### convert traj pickle to df
import os
import pandas as pd
import numpy as np
import pickle


class ConvertTrajectoryToStateDf:
	def __init__(self, getAllLevelsValueRange, getDfFromIndexLevelDict, extractColumnValues):
		self.getAllLevelsValueRange = getAllLevelsValueRange
		self.getDfFromIndexLevelDict = getDfFromIndexLevelDict
		self.extractColumnValues = extractColumnValues

	def __call__(self, trajectory):
		indexLevels = {levelName: getLevelValueRange(trajectory) for levelName, getLevelValueRange in
		               self.getAllLevelsValueRange.items()}
		emptyDf = self.getDfFromIndexLevelDict(indexLevels)
		extractTrajectoryInformation = lambda df: pd.Series({columnName: extractColumnValue(trajectory, df) for
		                                                     columnName, extractColumnValue in
		                                                     self.extractColumnValues.items()})
		stateDf = emptyDf.groupby(list(indexLevels.keys())).apply(extractTrajectoryInformation)

		return stateDf

class GetAgentCoordinateFromTrajectoryAndStateDf:
	def __init__(self, coordinates):
		self.coordinates = coordinates

	def __call__(self, trajectory, df):
		timeStep = df.index.get_level_values('timeStep')[0]
		objectId = df.index.get_level_values('agentId')[0]
		coordinates = trajectory[timeStep][objectId][self.coordinates]

		return coordinates

def saveToPickle(data, path):
	pklFile = open(path, "wb")
	pickle.dump(data, pklFile)
	pklFile.close()

def conditionDfFromParametersDict(parametersDict):
	levelNames = list(parametersDict.keys())
	levelValues = list(parametersDict.values())
	modelIndex = pd.MultiIndex.from_product(levelValues, names=levelNames)
	conditionDf = pd.DataFrame(index=modelIndex)
	return conditionDf
def main():


	getRangeNumAgentsFromTrajectory = lambda trajectory: list(range(np.shape(trajectory[0])[0]))
	getRangeTrajectoryLength = lambda trajectory: list(range(len(trajectory)))
	getAllLevelValuesRange = {'timeStep': getRangeTrajectoryLength, 'agentId': getRangeNumAgentsFromTrajectory}

	getAgentPosXCoord = GetAgentCoordinateFromTrajectoryAndStateDf(0)
	getAgentPosYCoord = GetAgentCoordinateFromTrajectoryAndStateDf(1)
	extractColumnValues = {'xPos': getAgentPosXCoord, 'yPos': getAgentPosYCoord}    	
	convertTrajectoryToStateDf = ConvertTrajectoryToStateDf(getAllLevelValuesRange, conditionDfFromParametersDict,extractColumnValues)

	dataFileDir = '../PataData'	
	trajectories=pd.read_pickle(os.path.join(dataFileDir, 'condition=1.pickle'))


	# for conditionParameters in conditionParametersAll:

	numTrajectories = len(trajectories)
	maxNumTrajectories = 5
	numTrajectoryChoose = min(numTrajectories, maxNumTrajectories)
	selectedTrajectories = trajectories[0:numTrajectoryChoose]

	selectedDf = [convertTrajectoryToStateDf(trajectory) for trajectory in selectedTrajectories]
	print(selectedDf)



	[saveToPickle(df, os.path.join(dataFileDir, 'condition=1sampleIndex={}.pickle'.format(sampleIndex))) for df, sampleIndex in zip(selectedDf, range(numTrajectories))]



if __name__ == '__main__':
    main()
