__author__ = 'mhjang'


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
