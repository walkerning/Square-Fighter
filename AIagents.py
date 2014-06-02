# -*- coding: utf-8 -*-
# AI agents


import game
from game import printNotDefined,manhattanDistance
import random

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

            if len(gameState.getLegalActions(self.index)) == 0 and gameState.getScores(self.index) > gameState.getScores(1 - self.index) :
                return -999
            if len(gameState.getLegalActions(1 - self.index)) == 0 and gameState.getScores(self.index) < gameState.getScores(1 - self.index) :
                return 999

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


from loopLearn import extractFeatures, FEATURES

class ReflexLinearAgent(Agent):
    def __init__(self, index, evalFunc = evalFunc):
        Agent.__init__(self, index)

        self.weights = (0.80559, -1.96247, 1.05913, -0.49355)
        self.evalFunc = evalFunc

    def setWeight(self, weights):
        self.weights = tuple(weights)

    def getAction(self, gameState):
        return max(gameState.getLegalActions(self.index), key = lambda action: self.evalFunc(gameState.generateSuccessor(self.index, action), self.index, self.weights))

from StateLearn import evalFunc

class ReflexStateAgent(Agent):
    def __init__(self, index, evalFunc = evalFunc):
        Agent.__init__(self, index)

        self.gameStateValue = [[{} for x in range(21)] for y in range(2)]
        self.evalFunc = evalFunc

    def setValue(self, gameStateLib):
        self.gameStateValue = gameStateLib

    def getAction(self, gameState):
        leftnum = len(gameState.getLeftPiles(self.index))
        legalaction = gameState.getLegalActions(self.index)
        max = -99999
        bestaction = legalaction[0]
        for action in legalaction:
            newgameState = gameState.generateSuccessor(self.index, action)
            #print str(newgameState.getBoard()) in self.gameStateValue[leftnum - 1].keys()
            if str(newgameState.getBoard()) in self.gameStateValue[self.index][leftnum - 1].keys():
                if self.gameStateValue[self.index][leftnum - 1][str(newgameState.getBoard())] > max:
                    bestaction = action
                    max = self.gameStateValue[self.index][leftnum - 1][str(newgameState.getBoard())]
            else:
                if self.evalFunc(newgameState, self.index) * 1.1 > max:
                    bestaction = action
                    max = self.evalFunc(newgameState, self.index) * 1.1

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

rlAgent = ReflexLinearAgent
rAgent = ReflexAgent
rsAgent = ReflexStateAgent
defaultAgent = rlAgent
abAgent = AlphaBetaAgent
srAgent = stupidReverseAgent
