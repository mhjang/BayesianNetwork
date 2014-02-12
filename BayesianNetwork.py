__author__ = 'mhjang'

import numpy as np
import itertools
from itertools import *

class Node:
    def __init__(self, name, valueLabel, idx):
        self.parents = list()
        self.name = name
        self.valueLabel = valueLabel
        self.idx = idx
    def setValue(self, value):
        self.value = value
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
            self.name == other.name and self.value == other.value)
    def __ne__(self, other):
        return not self.__eq__(other)
    def addParent(self, parentNode):
        self.parents.append(parentNode)
    def assignObservedData(self, data):
        self.observedData = data
    def getParents(self):
        return self.parents
    def getDataList(self, value):
        assert(value in self.valueLabel)
        return self.observedData[value]
    def printNodeInfo(self):
        print(self.valueLabel)
    def printParents(self):
        print(self.parents)
    def copy(self, value_):
        n = Node(self.name, self.valueLabel, self.idx)
        n.value = value_
        return n
    def __hash__(self):
        hashString = self.name + self.value
        return sum([ord(c) for c in hashString])


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

class CPT:
    def __init__(self, trainingFile):
        self.data = np.genfromtxt(trainingFile, delimiter=',')

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

def addChildren(parent, children):
    for child in children:
        child.addParent(parent)

# Initializing nodes
A = Node('A', {1:'<45',2:'45-55',3:'>=55'}, 0)
G = Node('G', {1:'Female',2:'Male'}, 1)
CP = Node('CP',{1:'Typical',2:'Atypical',3:'Non-Anginal', 4:'None'},2)
BP = Node('BP',{1:'Low', 2:'High'},3)
CH = Node('CH',{1:'Low', 2:'High'},4)
ECG = Node('ECG',{1:'Normal',2:'Abnormal'},5)
HR = Node('HR',{1:'Low',2:'High'},6)
EIA = Node('EIA', {1:'No', 2:'Yes'},7)
HD = Node('HD',{1:'No',2:'Yes'},8)
HD2 = Node('HD',{1:'No',2:'Yes'},8)


nodemap = {0:A, 1:G, 2:CP, 3:BP, 4:CH, 5:ECG, 6:HR, 7:EIA, 8:HD}

def predictHeartDisease(trainingFile, testFile):
    print("********** " + testFile + "************")
    cpt = CPT(trainingFile)
    hdprob = cpt.printCPT(HD, [CH, BP])
    hrprob = cpt.printCPT(HR, [A, HD])
    cpprob = cpt.printCPT(CP, [HD])
    eiaprob = cpt.printCPT(EIA, [HD])
    ecgprob = cpt.printCPT(ECG, [HD])
    denorm = 0

    CHValueMap = {value:key for (value, key) in CH.valueLabel.items()}
    BPValueMap = {value:key for (value, key) in BP.valueLabel.items()}
    CPValueMap = {value:key for (value, key) in CP.valueLabel.items()}
    EIAValueMap = {value:key for (value, key) in EIA.valueLabel.items()}
    ECGValueMap = {value:key for (value, key) in ECG.valueLabel.items()}
    AValueMap = {value:key for (value, key) in A.valueLabel.items()}
    HRValueMap = {value:key for (value, key) in HR.valueLabel.items()}

    f = open(testFile, 'r')
    lines = f.readlines()
    correctCount = 0
    wrongCount = 0
    for line in lines:
        elements = line.split(',')
        CHValue = CHValueMap[(int)(elements[CH.idx])]
        BPValue = BPValueMap[(int)(elements[BP.idx])]
        CPValue = CPValueMap[(int)(elements[CP.idx])]
        EIAValue = EIAValueMap[(int)(elements[EIA.idx])]
        ECGValue = ECGValueMap[(int)(elements[ECG.idx])]
        AValue = AValueMap[(int)(elements[A.idx])]
        HRValue = HRValueMap[(int)(elements[HR.idx])]
        HDAnswer = (int)(elements[HD.idx])

        CH_ = CH.copy(CHValue)
        CP_ = CP.copy(CPValue)
        BP_ = BP.copy(BPValue)
        EIA_ = EIA.copy(EIAValue)
        ECG_ = ECG.copy(ECGValue)
        A_ = A.copy(AValue)
        HR_ = HR.copy(HRValue)

        denorm = 0
        for hdv in HD.valueLabel.values():
            HD_ = HD.copy(hdv)
            denorm = denorm + hdprob[CPTInstance(HD_, [CH_, BP_])] + hrprob[CPTInstance(HR_, [A_, HD_])] \
                     + cpprob[CPTInstance(CP_, [HD_])] + eiaprob[CPTInstance(EIA_, [HD_])] + \
                    ecgprob[CPTInstance(ECG_, [HD_])]

        YesHD = HD.copy("Yes")
        norm = hdprob[CPTInstance(YesHD, [CH_, BP_])] + hrprob[CPTInstance(HR_, [A_, YesHD])] \
                                                     + cpprob[CPTInstance(CP_, [YesHD])] + eiaprob[CPTInstance(EIA_, [YesHD])] + \
                                                     ecgprob[CPTInstance(ECG_, [YesHD])]
        if norm/denorm >= 0.5000:
            predictValue = 2
        else:
            predictValue = 1
        if predictValue == HDAnswer:
            correctCount = correctCount + 1
        else:
            wrongCount = wrongCount + 1
    print("accuracy: " + str(correctCount / (correctCount + wrongCount)))
    return (correctCount) / (correctCount + wrongCount)

# Problem 4
def printCPT():
    prob2 = CPT("data-train-1.txt")
    # 4(a)
    aprob = prob2.printCPT(A, [])
    # 4(b)
    bpprob = prob2.printCPT(BP, [G])
    # 4(c)
    hdprob = prob2.printCPT(HD, [CH, BP])
    # 4(d)
    hrprob = prob2.printCPT(HR, [HD, BP, A])

# Problem 5
def probabilityQuery():
    cpt = CPT("data-train-1.txt")

    ## Query 1
    hdprob = cpt.printCPT(HD, [CH, BP])
    HD_ = HD.copy("No")
    CH_ = CH.copy("Low")
    BP_ = BP.copy("Low")

    chprob = cpt.printCPT(CH, [A, G])
    A_ = A.copy("45-55")
    G_ = G.copy("Male")
    denorm = 0
    for value in CH_.valueLabel.values():
        CH_ = CH.copy(value)
        denorm = denorm + chprob[CPTInstance(CH_, [A_, G_])] * hdprob[CPTInstance(HD_, [CH_, BP_])]

    for value in CH_.valueLabel.values():
        CH_ = CH.copy(value)
        print("CH = " + str(value), end = '')
        probability = chprob[CPTInstance(CH_, [A_, G_])] * hdprob[CPTInstance(HD_, [CH_, BP_])] / denorm
        print(str(probability))

    # Query 2
    bpprob = cpt.printCPT(BP, [G])
    hrprob = cpt.printCPT(HR, [HD, BP, A])
    hdprob = cpt.printCPT(HD, [CH, BP])

    A_ = A.copy('45-55')
    HD_ = HD.copy("No")
    HR_ = HR.copy("High")
    CH_ = CH.copy("High")

    denorm = 0
    for value in BP.valueLabel.values():
        BP_ = BP.copy(value)
        for gvalue in G.valueLabel.values():
            G_ = G.copy(gvalue)
            denorm = denorm + bpprob[CPTInstance(BP_, [G_])] * hrprob[CPTInstance(HR_, [HD_, BP_, A_])] * hdprob[CPTInstance(HD_, [CH_, BP_])]

    for value in BP.valueLabel.values():
        BP_ = BP.copy(value)
        norm = 0
        for gvalue in G.valueLabel.values():
            G_ = G.copy(gvalue)
            norm = norm + bpprob[CPTInstance(BP_, [G_])] * hrprob[CPTInstance(HR_, [HD_, BP_, A_])] * hdprob[CPTInstance(HD_, [CH_, BP_])]
        print("BP = " + str(value), end = ': ')
        print(str(norm / denorm))



def predictHeartDiseaseForNewModel(trainingFile, testFile):
    print("********** " + testFile + "************")
    cpt = CPT(trainingFile)
    hdprob = cpt.printCPT(HD, [BP])
    hrprob = cpt.printCPT(HR, [A, HD])
    cpprob = cpt.printCPT(CP, [HD])
    eiaprob = cpt.printCPT(EIA, [HD])
    ecgprob = cpt.printCPT(ECG, [HD])
    denorm = 0

    CHValueMap = {value:key for (value, key) in CH.valueLabel.items()}
    BPValueMap = {value:key for (value, key) in BP.valueLabel.items()}
    CPValueMap = {value:key for (value, key) in CP.valueLabel.items()}
    EIAValueMap = {value:key for (value, key) in EIA.valueLabel.items()}
    ECGValueMap = {value:key for (value, key) in ECG.valueLabel.items()}
    AValueMap = {value:key for (value, key) in A.valueLabel.items()}
    HRValueMap = {value:key for (value, key) in HR.valueLabel.items()}

    f = open(testFile, 'r')
    lines = f.readlines()
    correctCount = 0
    wrongCount = 0
    for line in lines:
        elements = line.split(',')
        CHValue = CHValueMap[(int)(elements[CH.idx])]
        BPValue = BPValueMap[(int)(elements[BP.idx])]
        CPValue = CPValueMap[(int)(elements[CP.idx])]
        EIAValue = EIAValueMap[(int)(elements[EIA.idx])]
        ECGValue = ECGValueMap[(int)(elements[ECG.idx])]
        AValue = AValueMap[(int)(elements[A.idx])]
        HRValue = HRValueMap[(int)(elements[HR.idx])]
        HDAnswer = (int)(elements[HD.idx])

        CH_ = CH.copy(CHValue)
        CP_ = CP.copy(CPValue)
        BP_ = BP.copy(BPValue)
        EIA_ = EIA.copy(EIAValue)
        ECG_ = ECG.copy(ECGValue)
        A_ = A.copy(AValue)
        HR_ = HR.copy(HRValue)

        denorm = 0
        for hdv in HD.valueLabel.values():
            HD_ = HD.copy(hdv)
            denorm = denorm + hdprob[CPTInstance(HD_, [BP_])] + hrprob[CPTInstance(HR_, [A_, HD_])] \
                     + cpprob[CPTInstance(CP_, [HD_])] + eiaprob[CPTInstance(EIA_, [HD_])] + \
                    ecgprob[CPTInstance(ECG_, [HD_])]

        YesHD = HD.copy("Yes")
        norm = hdprob[CPTInstance(YesHD, [BP_])] + hrprob[CPTInstance(HR_, [A_, YesHD])] \
                                                     + cpprob[CPTInstance(CP_, [YesHD])] + eiaprob[CPTInstance(EIA_, [YesHD])] + \
                                                     ecgprob[CPTInstance(ECG_, [YesHD])]
        if norm/denorm >= 0.5000:
            predictValue = 2
        else:
            predictValue = 1
        if predictValue == HDAnswer:
            correctCount = correctCount + 1
        else:
            wrongCount = wrongCount + 1
    print("accuracy: " + str(correctCount / (correctCount + wrongCount)))
    return (correctCount) / (correctCount + wrongCount)

def main():

####### Problem 4 ######
#    printCPT()

####### Problem 5 ######
#    probabilityQuery()

##### for problem 6 ######
#    trainingSet = ['data-train-1.txt', 'data-train-2.txt', 'data-train-3.txt', 'data-train-4.txt', 'data-train-5.txt']
#    testSet = ['data-test-1.txt', 'data-test-2.txt', 'data-test-3.txt', 'data-test-4.txt', 'data-test-5.txt']
#    result = [predictHeartDiseaseForModel(training, test)  for (training, test) in zip(trainingSet, testSet)]
#    print(np.average(result), np.std(result))

##### for problem 7 #####
    trainingSet = ['data-train-1.txt', 'data-train-2.txt', 'data-train-3.txt', 'data-train-4.txt', 'data-train-5.txt']
    testSet = ['data-test-1.txt', 'data-test-2.txt', 'data-test-3.txt', 'data-test-4.txt', 'data-test-5.txt']
    result = [predictHeartDiseaseForNewModel(training, test)  for (training, test) in zip(trainingSet, testSet)]
    print(np.average(result), np.std(result))

if __name__ == "__main__":
    main()

#for i in range(9):
#    nodeIdx[i].assignObservedData(dataDic[i])

