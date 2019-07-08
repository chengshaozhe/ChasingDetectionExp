
class Experiment():
    def __init__(self, trial, writer, experimentValues):
        self.trial = trial
        self.writer = writer
        self.experimentValues = experimentValues

    def __call__(self, designValues):
        for trialIndex in range(len(designValues)):
            condition = designValues[trialIndex]
            results = self.trial(condition)
            results["trail"] = trialIndex + 1
            results["condition"] = condition
            print(results)
            response = self.experimentValues.copy()
            response.update(results)
            self.writer(response, trialIndex)
        return results
