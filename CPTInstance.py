__author__ = 'mhjang'


class CPTInstance:
    def __init__(self, var, condVar):
        self.var = var
        self.condVar = condVar
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.var == other.var and set(self.condVar) == set(other.condVar))
    def __ne__(self, other):
        return not __eq__(self, other)
    def __getHashKey__(self, str):
        return sum([ord(c) for c in str])

    def __hash__(self):
        hashKey = 0
        for var in self.condVar:
            hashKey = hashKey + self.__getHashKey__(var.name)
        hashKey = hashKey + self.__getHashKey__(self.var.name)
        return hashKey

    # generate a vector that sets the conditional variable to 1 and 0 to the others
    def generateSettingVec(self, vars):
        numOfCombination = 1
        for i in range(len(vars)):
            numOfCombination = numOfCombination * len(vars[i].valueLabel)
        settings = np.zeros((numOfCombination,9))
        if len(vars) == 4:
            var1Idx = vars[0].idx
            var2Idx = vars[1].idx
            var3Idx = vars[2].idx
            var4Idx = vars[3].idx
            combinations = itertools.product(vars[0].valueLabel.keys(), vars[1].valueLabel.keys(), vars[2].valueLabel.keys(), vars[3].valueLabel.keys())
            idx = 0
            for element in combinations:
                settings[idx][var1Idx] = element[0]
                settings[idx][var2Idx] = element[1]
                settings[idx][var3Idx] = element[2]
                settings[idx][var4Idx] = element[3]
                idx = idx + 1
        elif len(vars) == 3:
            var1Idx = vars[0].idx
            var2Idx = vars[1].idx
            var3Idx = vars[2].idx
            combinations = itertools.product(vars[0].valueLabel.keys(), vars[1].valueLabel.keys(), vars[2].valueLabel.keys())
            idx = 0
            for element in combinations:
                settings[idx][var1Idx] = element[0]
                settings[idx][var2Idx] = element[1]
                settings[idx][var3Idx] = element[2]
                idx = idx + 1

        elif len(vars) == 2:
            var1Idx = vars[0].idx
            var2Idx = vars[1].idx
            combinations = itertools.product(vars[0].valueLabel.keys(), vars[1].valueLabel.keys())
            idx = 0
            for element in combinations:
                settings[idx][var1Idx] = element[0]
                settings[idx][var2Idx] = element[1]
                idx = idx + 1
        elif len(vars) == 1:
            var1Idx = vars[0].idx
            combinations = vars[0].valueLabel.keys()
            idx = 0
            for element in combinations:
                settings[idx][var1Idx] = element
                idx = idx + 1
        return settings
