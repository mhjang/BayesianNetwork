__author__ = 'mhjang'
import itertools
import numpy as np
from CPTInstance import CPTInstance

class CPT:
    def __init__(self, trainingFile):
        self.data = np.genfromtxt(trainingFile, delimiter=',')
        print(trainingFile)
    def printCPT(self, var, condVar):
        # location where values are set
        allVar = list(condVar)
        allVar.append(var)
        settings = self.generateSettingVec(allVar)
        cptdic = {}
        for vector in settings:
         ###### for conditional variables
            valueList = np.array(np.nonzero(vector))[0]
            occurenceVector = [np.transpose(self.data[:,valueLoc]==vector[valueLoc]) for valueLoc in valueList]
            init = occurenceVector[0]
            for vec in occurenceVector:
                init = np.logical_and(vec, init)
            norm = np.sum(init)
      #      print(vector)
            if len(condVar) > 0:
             ###### for variables
                vectorWithoutVar = np.copy(vector)
                vectorWithoutVar[var.idx] = 0
                valueList2 = np.array(np.nonzero(vectorWithoutVar))[0]
                occurenceVector = [np.transpose(self.data[:,valueLoc]==vectorWithoutVar[valueLoc]) for valueLoc in valueList2]

                init2 = occurenceVector[0]
                for vec in occurenceVector:
                    init2 = np.logical_and(vec, init2)
                denorm = np.sum(init2)

            else:
                denorm = len(self.data)

            # instance of a condintional variables with values
            varInstance = var.copy(var.valueLabel[vector[var.idx]])
            print(varInstance.name + "=" + str(varInstance.valueLabel[vector[varInstance.idx]]), end = " ")

            condVarInstance = list()
            for node in condVar[::-1]:
                print(node.name + "=" + str(node.valueLabel[vector[node.idx]]), end = " ")
                n = node.copy(node.valueLabel[vector[node.idx]])
                condVarInstance.append(n)

            cptins = CPTInstance(varInstance, condVarInstance)
            print("Probabilty:" +str(norm/denorm))
            cptdic[cptins] = (norm/denorm)
        return cptdic


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
