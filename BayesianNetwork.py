__author__ = 'mhjang'

import numpy as np
from Node import Node
from CPT import CPT
from CPTInstance import CPTInstance


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


nodemap = {0:A, 1:G, 2:CP, 3:BP, 4:CH, 5:ECG, 6:HR, 7:EIA, 8:HD}

def predictHeartDisease(trainingFile, testFile):
    print("********** " + testFile + "************")
    cpt = CPT(trainingFile)
    hdprob = cpt.printCPT(HD, [CH, BP])
    hrprob = cpt.printCPT(HR, [BP, A, HD])
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
            denorm = denorm + hdprob[CPTInstance(HD_, [CH_, BP_])] * hrprob[CPTInstance(HR_, [BP_, A_, HD_])] \
                     * cpprob[CPTInstance(CP_, [HD_])] * eiaprob[CPTInstance(EIA_, [HD_])] *  \
                    ecgprob[CPTInstance(ECG_, [HD_])]

        YesHD = HD.copy("Yes")
        norm1 = hdprob[CPTInstance(YesHD, [CH_, BP_])] * hrprob[CPTInstance(HR_, [BP_, A_, YesHD])] \
                                                     * cpprob[CPTInstance(CP_, [YesHD])] * eiaprob[CPTInstance(EIA_, [YesHD])] * \
                                                     ecgprob[CPTInstance(ECG_, [YesHD])]
        NoHD = HD.copy("No")
        norm2 = hdprob[CPTInstance(NoHD, [CH_, BP_])] * hrprob[CPTInstance(HR_, [BP_, A_, NoHD])] \
                                                     * cpprob[CPTInstance(CP_, [NoHD])] * eiaprob[CPTInstance(EIA_, [NoHD])] * \
                                                     ecgprob[CPTInstance(ECG_, [NoHD])]

        if norm1/denorm >= norm2/denorm:
            predictValue = 2
        else:
            predictValue = 1
        if predictValue == HDAnswer:
            correctCount = correctCount + 1
        else:
            wrongCount = wrongCount + 1
    print("accuracy: " + str(correctCount / (correctCount + wrongCount)))
 #   print(correctCount, wrongCount)
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
    gprob = cpt.printCPT(G, [])
    chprob = cpt.printCPT(CH, [A, G])
    A_ = A.copy('45-55')
    HD_ = HD.copy("No")
    HR_ = HR.copy("High")
    CH_ = CH.copy("High")

    denorm = 0
    for value in BP.valueLabel.values():
        BP_ = BP.copy(value)
        for gvalue in G.valueLabel.values():
            G_ = G.copy(gvalue)
            denorm = denorm + bpprob[CPTInstance(BP_, [G_])] * hrprob[CPTInstance(HR_, [HD_, BP_, A_])] * hdprob[CPTInstance(HD_, [CH_, BP_])] * gprob[CPTInstance(G_, [])] * chprob[CPTInstance(CH_, [A_, G_])]

    for value in BP.valueLabel.values():
        BP_ = BP.copy(value)
        norm = 0
        for gvalue in G.valueLabel.values():
            G_ = G.copy(gvalue)
            norm = norm + bpprob[CPTInstance(BP_, [G_])] * hrprob[CPTInstance(HR_, [HD_, BP_, A_])] * hdprob[CPTInstance(HD_, [CH_, BP_])] * gprob[CPTInstance(G_, [])] * chprob[CPTInstance(CH_, [A_, G_])]
        print("BP = " + str(value), end = ': ')
        print(str(norm / denorm))



def predictHeartDiseaseForNewModel(trainingFile, testFile):
    print("********** " + testFile + "************")
    cpt = CPT(trainingFile)
    bprob = cpt.printCPT(BP, [])
    hdprob = cpt.printCPT(HD, [BP])
    hrprob = cpt.printCPT(HR, [A, BP, HD])
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
            denorm = denorm + hdprob[CPTInstance(HD_, [BP_])] * hrprob[CPTInstance(HR_, [BP_, A_, HD_])] \
                     * cpprob[CPTInstance(CP_, [HD_])] * eiaprob[CPTInstance(EIA_, [HD_])] *  \
                    ecgprob[CPTInstance(ECG_, [HD_])]

        YesHD = HD.copy("Yes")
        norm = hdprob[CPTInstance(YesHD, [BP_])] * hrprob[CPTInstance(HR_, [BP_, A_, YesHD])] \
                                                     * cpprob[CPTInstance(CP_, [YesHD])] * eiaprob[CPTInstance(EIA_, [YesHD])] * \
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
    printCPT()

####### Problem 5 ######
#    probabilityQuery()

##### for problem 6 ######
 #   trainingSet = ['data-train-1.txt', 'data-train-2.txt', 'data-train-3.txt', 'data-train-4.txt', 'data-train-5.txt']
 #   testSet = ['data-test-1.txt', 'data-test-2.txt', 'data-test-3.txt', 'data-test-4.txt', 'data-test-5.txt']
 #   result = [predictHeartDisease(training, test) for (training, test) in zip(trainingSet, testSet)]
 #   print(np.average(result), np.std(result))

##### for problem 7 #####
    trainingSet = ['data-train-1.txt', 'data-train-2.txt', 'data-train-3.txt', 'data-train-4.txt', 'data-train-5.txt']
    testSet = ['data-test-1.txt', 'data-test-2.txt', 'data-test-3.txt', 'data-test-4.txt', 'data-test-5.txt']
    result = [predictHeartDiseaseForNewModel(training, test)  for (training, test) in zip(trainingSet, testSet)]
    print(np.average(result), np.std(result))

if __name__ == "__main__":
    main()

#for i in range(9):
#    nodeIdx[i].assignObservedData(dataDic[i])

