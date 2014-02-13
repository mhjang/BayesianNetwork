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

