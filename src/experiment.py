import numpy as np
class Experiment():
    def __init__(self, trial, writer, experimentValues,darwImage,restImage,darwBackground,hasRest=True):
        self.trial = trial
        self.writer = writer
        self.experimentValues = experimentValues
        self.darwImage=darwImage
        self.restImage=restImage
        self.darwBackground=darwBackground
        self.hasRest=hasRest
    def __call__(self, designValues,restDuration):
        for trialIndex in range(len(designValues)):          
            condition = designValues[trialIndex]
            results = self.trial(condition)
            results["trail"] = trialIndex + 1
            results["condition"] = condition
            response = self.experimentValues.copy()
            response.update(results)
            self.writer(response, trialIndex)
            if np.mod(trialIndex+1,restDuration)==0 & self.hasRest:
                self.darwBackground()
                self.darwImage(self.restImage)  
        return results
