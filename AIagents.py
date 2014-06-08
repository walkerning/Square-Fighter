# -*- coding: utf-8 -*-
# AI agents


import game
from game import printNotDefined,manhattanDistance
import random
from qLearn import DATA_FILENAME
import util

DATA_FILENAMEFORSTATE = "g:\\shuju.txt"

class Agent(object):
    """
    An agent must define the getAction method which will be called with a GameState argument.
    The getAction method should return an action, which is a three-element tuple (pileIndex, squarePos, rotateIndex)
    The pileIndex refer to the index of the pile that will be placed; it's a integer.
    The squarePos refer to the position on the board of the reference square of the specific pile; it's a two-int-tuple.
    The rotateIndex refer to the index of the rotation of the pile; it's a integer.
    """
    def __init__(self, index):
        self.index = index

    def getAction(self, gameState):
        raiseNotDefined()

class stupidAgent(Agent):
    def getAction(self, gameState):
        return gameState.getLegalActions(self.index)[0]

class stupidRandomAgent(Agent):
    def getAction(self, gameState):
        import random
        return random.choice(gameState.getLegalActions(self.index))

class stupidReverseAgent(Agent):
    def getAction(self, gameState):
        return gameState.getLegalActions(self.index)[-1]

from loopLearn import evalFunc

class AlphaBetaAgent(Agent):
    def __init__(self, index, evalFunc = evalFunc):
        Agent.__init__(self, index)

        self.weights = (0.7317122, -1.951789, 0.1245964, -0.763426, 2.031588)
        self.evalFunc = evalFunc

    def getAction(self, gameState):
        self.depth = 1
        def alphabeta(depth, gameState, agentIndex, alpha, beta):

            if agentIndex == self.index:
                v = -99999
                if depth != self.depth:
                    for move in gameState.getLegalActions(agentIndex):
                        v = max(alphabeta(depth, gameState.generateSuccessor(agentIndex,move), 1 - agentIndex, alpha, beta), v)
                        if v >= beta:
                            return v
                        alpha = max(alpha,v)
                    return v
                else:
                    legalaction = gameState.getLegalActions(agentIndex)
                    count = []
                    for move in legalaction:
                        count += [alphabeta(depth, gameState.generateSuccessor(agentIndex,move), 1 - agentIndex, alpha, beta)]
                        if max(count) >= beta:
                            return move
                    return legalaction[count.index(max(count))]

            else:
                depth -= 1

                if depth == 0:
                    return self.evalFunc(gameState, self.index, self.weights)

                v = 99999
                for move in gameState.getLegalActions(agentIndex):
                    v = min(alphabeta(depth, gameState.generateSuccessor(agentIndex,move), 1 - agentIndex, alpha, beta), v)
                    if v <= alpha:
                        return v
                    beta = min(beta,v)
                return v

        tmp = alphabeta(self.depth, gameState, self.index, -99999, 99999)
        return tmp
    '''
    def evaluationFunction(self, gameState):
        theta = [0.5 for i in range(5)]
        otherDetails = 0
        singlegridlist = []
        for grid in gameState._getAvailableAndImportantGrids(self.index)[0]:
            if (grid[0] + 1, grid [1] + 1) not in gameState._getAvailableAndImportantGrids(self.index)[0] and (grid[0] + 1, grid [1] - 1) not in gameState._getAvailableAndImportantGrids(self.index)[0] and (grid[0] - 1, grid [1] + 1) not in gameState._getAvailableAndImportantGrids(self.index)[0] and (grid[0] - 1, grid [1] - 1) not in gameState._getAvailableAndImportantGrids(self.index)[0]:
                singlegridlist.append(grid)
        for grid in singlegridlist:
            for grid2 in singlegridlist[singlegridlist.index(grid):]:
                if manhattanDistance(grid, grid2) == 2:
                    otherDetails += 5
        return - 5 * gameState.getScores(self.index) + len(gameState._getAvailableAndImportantGrids(self.index)[1]) - 30 * len(gameState._getAvailableAndImportantGrids(1 - self.index)[1]) + otherDetails
    '''
class ReflexAgent(Agent):
 
  def getAction(self, gameState):
    # Collect legal moves and successor states
    self.legalMoves = gameState.getLegalActions(self.index)

    # Choose one of the best actions
    score = -9999
    i = 0
    j = 0
    for action in self.legalMoves:
        newscore = self.evaluationFunction(gameState.generateSuccessor(self.index, action))
        if newscore > score :
            score = newscore
            j = i
        i += 1

    return self.legalMoves[j]

  def evaluationFunction(self, gameState):
    theta = [0.5 for i in range(5)]
    otherDetails = 0
    singlegridlist = []
    for grid in gameState._getAvailableAndImportantGrids(self.index)[0]:
        if (grid[0] + 1, grid [1] + 1) not in gameState._getAvailableAndImportantGrids(self.index)[0] and (grid[0] + 1, grid [1] - 1) not in gameState._getAvailableAndImportantGrids(self.index)[0] and (grid[0] - 1, grid [1] + 1) not in gameState._getAvailableAndImportantGrids(self.index)[0] and (grid[0] - 1, grid [1] - 1) not in gameState._getAvailableAndImportantGrids(self.index)[0]:
            singlegridlist.append(grid)
    for grid in singlegridlist:
        for grid2 in singlegridlist[singlegridlist.index(grid):]:
            if manhattanDistance(grid, grid2) == 2:
                otherDetails += 5
    return - 5 * gameState.getScores(self.index) + len(gameState._getAvailableAndImportantGrids(self.index)[1]) - 20 * len(gameState._getAvailableAndImportantGrids(1 - self.index)[1]) + otherDetails



from loopLearn import extractFeatures, FEATURES, evalFunc

class ReflexLinearAgent(Agent):
    def __init__(self, index, evalFunc = evalFunc):
        Agent.__init__(self, index)

        self.weights = (0.7317, -1.9518, 0.1246, -0.7634, 2.0316)#(1.0516153729117497, -1.7406298037151497, 2.2668134620369664, -1.705074288351434)#(0.80559, -1.96247, 1.05913, -0.49355)
        self.evalFunc = evalFunc

    def setWeight(self, weights):
        self.weights = tuple(weights)

    def getAction(self, gameState):
        return max(gameState.getLegalActions(self.index), key = lambda action: self.evalFunc(gameState.generateSuccessor(self.index, action), self.index, self.weights))

from StateLearn import evalFunc

class ReflexStateAgent(Agent):
    def __init__(self, index, evalFunc = evalFunc):
        Agent.__init__(self, index)

        self.evalFunc = evalFunc
        self.k = 2

    def setValue(self, gameStateLib):
        self.gameStateValue = gameStateLib

    def setKValue(self, k):
        self.k = k

    def getAction(self, gameState):
        leftnum = len(gameState.getLeftPiles(self.index))
        legalaction = gameState.getLegalActions(self.index)
        sumprob = 0
        max = -99999
        dist = util.Counter()
        bestaction = legalaction[0]
        for action in legalaction:
            newgameState = gameState.generateSuccessor(self.index, action)
            #print str(newgameState.getBoard()) in self.gameStateValue[leftnum - 1].keys()
            if str(newgameState.getBoard()) in self.gameStateValue[self.index][leftnum - 1].keys():
                '''
                if self.gameStateValue[self.index][leftnum - 1][str(newgameState.getBoard())] > max:
                    bestaction = action
                    max = self.gameStateValue[self.index][leftnum - 1][str(newgameState.getBoard())]
                '''
                print "!!"
                sumprob += (self.k ** self.gameStateValue[self.index][leftnum - 1][str(newgameState.getBoard())])
            else:
                '''
                if self.evalFunc(newgameState, self.index) * 1.9 > max:
                    bestaction = action
                    max = self.evalFunc(newgameState, self.index) * 1.9
                '''
                sumprob += (self.k ** self.evalFunc(newgameState, self.index))
        for action in legalaction:
            newgameState = gameState.generateSuccessor(self.index, action)
            if str(newgameState.getBoard()) in self.gameStateValue[self.index][leftnum - 1].keys():
                dist[action] = (self.k ** self.gameStateValue[self.index][leftnum - 1][str(newgameState.getBoard())]) / sumprob
            else:
                dist[action] = (self.k ** self.evalFunc(newgameState, self.index)) / sumprob

        dist.normalize()

        return util.chooseFromDistribution( dist )
        return bestaction

class ReflexLearnedAgent(Agent):
    def __init__(self, index, evalFunc = evalFunc):
        Agent.__init__(self, index)

        import time, cPickle
        f = open(DATA_FILENAMEFORSTATE)
        try:
            self.gameStateValue = cPickle.load(f)
        except:
            print "oops"
            return
        finally:
            f.close()
        
        self.evalFunc = evalFunc

    def getAction(self, gameState):
        leftnum = len(gameState.getLeftPiles(self.index))
        legalaction = gameState.getLegalActions(self.index)
        sumprob = 0
        max = -99999
        bestaction = legalaction[0]
        for action in legalaction:
            newgameState = gameState.generateSuccessor(self.index, action)
            if str(newgameState.getBoard()) in self.gameStateValue[self.index][leftnum - 1].keys():
                print "in"
                if self.gameStateValue[self.index][leftnum - 1][str(newgameState.getBoard())] > max:
                    bestaction = action
                    max = self.gameStateValue[self.index][leftnum - 1][str(newgameState.getBoard())]
            else:
                if self.evalFunc(newgameState, self.index) > max:
                    bestaction = action
                    max = self.evalFunc(newgameState, self.index)
        return bestaction


class ReflexAgent(Agent):

  def getAction(self, gameState):
    # Collect legal moves and successor states
    self.legalMoves = gameState.getLegalActions(self.index)

    # Choose one of the best actions
    score = -9999
    i = 0
    j = 0
    for action in self.legalMoves:
        newscore = self.evaluationFunction(gameState.generateSuccessor(self.index, action))
        if newscore > score :
            score = newscore
            j = i
        i += 1

    return self.legalMoves[j]

  def evaluationFunction(self, gameState):
    theta = [0.5 for i in range(5)]
    otherDetails = 0
    singlegridlist = []
    for grid in gameState._getAvailableAndImportantGrids(self.index)[0]:
        if (grid[0] + 1, grid [1] + 1) not in gameState._getAvailableAndImportantGrids(self.index)[0] and (grid[0] + 1, grid [1] - 1) not in gameState._getAvailableAndImportantGrids(self.index)[0] and (grid[0] - 1, grid [1] + 1) not in gameState._getAvailableAndImportantGrids(self.index)[0] and (grid[0] - 1, grid [1] - 1) not in gameState._getAvailableAndImportantGrids(self.index)[0]:
            singlegridlist.append(grid)
    for grid in singlegridlist:
        for grid2 in singlegridlist[singlegridlist.index(grid):]:
            if game.manhattanDistance(grid, grid2) == 2:
                otherDetails += 10
    return gameState.getScores(self.index) + len(gameState._getAvailableAndImportantGrids(self.index)[0]) - gameState.getScores(1 - self.index) - 2 * len(gameState._getAvailableAndImportantGrids(1 - self.index)[0]) + otherDetails


class qLearnAgent(Agent):
    def __init__(self, index, xl = False):
        Agent.__init__(self, index)

        if not xl:
            import cPickle
            f = open(DATA_FILENAME)
            try:
                self.rawStateLib = cPickle.load(f)
            except:
                print "oops!"
                import sys
                sys.exit(0)
            finally:
                f.close()

        self.xl = xl
        self.k = 2

    def setLib(self, lib):
        self.rawStateLib = lib

    def getAction(self, gameState):
        if not self.xl:
            return max(gameState.getLegalActions(self.index), key = lambda action: self.rawStateLib[gameState.generateSuccessor(self.index, action)][self.index])
        # 增加随机性
        sumprob = 0
        dist = util.Counter()
        for action in gameState.getLegalActions(self.index):
            newState = gameState.generateSuccessor(self.index, action)
            #sumprob += self.k ** self.rawStateLib[newState][self.index]
            dist[action] = (self.k ** self.rawStateLib[newState][self.index])
        dist.normalize()

        return util.chooseFromDistribution( dist )

rlAgent = ReflexLinearAgent
rAgent = ReflexAgent
rsAgent = ReflexStateAgent
rldAgent = ReflexLearnedAgent
defaultAgent = rlAgent
abAgent = AlphaBetaAgent
srAgent = stupidReverseAgent
qlAgent = qLearnAgent
