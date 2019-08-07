import numpy as np
class Experiment():
    def __init__(self, trial, writer, experimentValues,darwImage,restImage,):
        self.trial = trial
        self.writer = writer
        self.experimentValues = experimentValues
        self.darwImage=darwImage
        self.restImage=restImage
    def __call__(self, designValues,restDuration):
        for trialIndex in range(len(designValues)):          
            condition = designValues[trialIndex]
            print(condition)
            results = self.trial(condition)
            results["trail"] = trialIndex + 1
            results["condition"] = condition
            print(results)
            response = self.experimentValues.copy()
            response.update(results)
            self.writer(response, trialIndex)
            if np.mod(trialIndex+1,restDuration)==0:
                self.darwImage(self.restImage)  
        return results
