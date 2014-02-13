__author__ = 'mhjang'

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
