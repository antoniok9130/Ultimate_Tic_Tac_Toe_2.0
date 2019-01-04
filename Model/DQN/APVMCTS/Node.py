from numpy import sqrt, log

from UTTT.Node import *


c_puct = 4
class APVMCTS_Node(UTTT_Node):

    def __init__(self, pa, move = None, parent = None, initialize = False):
        super().__init__(move, parent, initialize)

        self.numVisits = 0
        self.totalAction = 0
        self.meanAction = 0
        self.priorProbability = pa
        self.value = 100
        self.oldValue = True


    # def updateUCT(self):
    #     if self.parent is not None and self.numVisits != 0:
    #         self.UCT = self.numWins/self.numVisits + sqrt(2*log(self.parent.getNumVisits())/self.numVisits)


    def getValue(self):
        if self.oldValue:
            if self.parent is not None:
                self.meanAction = 0 if self.numVisits == 0 else self.totalAction/self.numVisits
                self.value = calculateU(self.meanAction, self.priorProbability, self.numVisits, self.parent.numVisits)
            else:
                self.value = 100
            self.oldValue = False

        return self.value

    def incrementAction(self, num):
        self.totalAction += num
        self.numVisits += 1
        self.oldValue = True

    def get_priorities(self):
        total = sum(child.numVisits for child in self.children)
        priorities = np.zeros(81)
        for child in self.children:
            priorities[flatten_move(child.move)] = child.numVisits/total

        return priorities

        


    def getConfidence(self):
        if self.numVisits > 0:
            return self.meanAction
        
        return 0.5



    def setChild(self, move):
        if self.children is not None:
            for i, child in enumerate(self.children):
                if child.move[0] == move[0] and child.move[1] == move[1]:
                    self.children.insert(0, self.children.pop(i))
                    return

        elif self.isLegal(move):
            self.children = [self.__class__(0, move, self, True)]

        else:
            print("Could not find child with move:  {0} {1}".format(move[0], move[1]))
            exit(1)


@jit(cache=True, nopython=True)
def calculateU(meanAction, priorProbability, numVisits, parent_numVisits):
    return meanAction + c_puct*priorProbability*sqrt(parent_numVisits)/(1+numVisits)