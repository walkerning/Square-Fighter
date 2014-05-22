# -*- coding: utf-8 -*-
# AI agents


import game
from game import printNotDefined,manhattanDistance
from StateLearn import gameStateLib
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

class AlphaBetaAgent(Agent):
    def getAction(self, gameState):
        self.depth = 2
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
                    return self.evaluationFunction(gameState)

                v = 99999
                for move in gameState.getLegalActions(agentIndex):
                    v = min(alphabeta(depth, gameState.generateSuccessor(agentIndex,move), 1 - agentIndex, alpha, beta), v)
                    if v <= alpha:
                        return v
                    beta = min(beta,v)
                return v

        tmp = alphabeta(self.depth, gameState, self.index, -99999, 99999)
        return tmp

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


from learn import extractFeatures, FEATURES, evalFunc

class ReflexLinearAgent(Agent):
    def __init__(self, index, evalFunc = evalFunc):
        Agent.__init__(self, index)

        self.weights = (1.0516153729117497, -1.7406298037151497, 2.2668134620369664, -1.705074288351434)#(0.8910675658865255, -3.1839751011649087, -0.2879020903914638, -1.0871294643958471, 2.469392715066099)#(0.4034291420404963, -1.974784328730528, -0.7064027925005527, -1.6819318793652704, 1.207184735264548)
        self.evalFunc = evalFunc

    def setWeight(self, weights):
        self.weights = tuple(weights)

    def getAction(self, gameState):
        return max(gameState.getLegalActions(self.index), key = lambda action: self.evalFunc(gameState.generateSuccessor(self.index, action), self.index, self.weights))

from StateLearn import evalFunc

class ReflexStateAgent(Agent):
    def __init__(self, index, evalFunc = evalFunc):
        Agent.__init__(self, index)

        self.gameStateValue = [{} for x in range(21)]
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
            if newgameState in gameStateLib[leftnum - 1].keys():
                if gameStateLib[leftnum - 1][str(newgameState)] > max:
                    bestaction = action
                    max = gameStateLib[leftnum - 1][str(newgameState)]
            else:
                if self.evalFunc(newgameState, self.index) * 1.01 > max:
                    bestaction = action
                    max = self.evalFunc(newgameState, self.index) * 1.01
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
defaultAgent = stupidReverseAgent
abAgent = AlphaBetaAgent
srAgent = stupidReverseAgent
