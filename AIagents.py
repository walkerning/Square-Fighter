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


from loopLearn import extractFeatures, FEATURES, evalFunc

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

        self.gameStateValue = [{}, {}, {}, {'00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\neee0e0e0000100\n0e0ee00e1ee1e0\n000e0e001e11ee\neee001ee110011\n00e01111e10111\n00e0e000001000\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 71.52569932, '00e00e000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\neee0e0e0000100\n000ee00e1ee1e0\n0eee0e001e11ee\n0ee001ee110011\ne0e01111e10111\n00e0e000001000\n0e0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 68.05200996, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\n0e000e0e0ee1e0\n0ee0e0e0000100\neeeee00e1ee1e0\n000e0e001e11ee\n0ee001ee110011\n0ee01111e10111\neee0e000001000\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 67.30783812, '00e00e000e0000\ne00e00e0e0eeee\ne0e0eee0e0000e\n0e000e0e0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee110011\n0ee01111e10111\n00e0e000001000\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 72.14628624000001, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee10e\neeee0e001e11ee\n00e001ee110011\n0ee01111e10111\n00e0e000001000\nee0e0e11e11101\ne00e00011e1010\ne00eee0e1ee110\neee11111e11e11': 74.08329476, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\n0e000e0e0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee110011\n0ee01111e10111\n00e0e000001000\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 72.14628624000001, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\neee0e0e0000100\n000ee00e1ee1e0\n0e0e0e001e11ee\neee001ee110011\n00e01111e10111\n00e0e000001000\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 70.78152748, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\neee0e0e0000100\n0e0ee00e1ee1e0\n000e0e001e11ee\neee001ee110011\n0ee01111e10111\n0ee0e000001000\ne00e0e11e111e1\ne00e00011e1e1e\nee0eee0e1ee11e\neee11111e11e11': 68.06446960000001, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\n0e000e0e0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee110011\ne0e01111e10111\n00e0e000001000\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 72.14628624000001}, {'00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n0e0ee00e1ee1e0\n000e0e001e11ee\neee001ee110011\n0ee01111e10111\n0ee0e000001000\ne00e0e11e111e1\ne00e00011e1e1e\nee0eee0e1ee11e\neee11111e11e11': 66.70071084000001, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee110011\ne0e01111e10111\n00e0e000001000\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 70.78252748, '00ee000e0ee000\ne00e0e0ee0eee0\ne0e0eeeee0000e\nee000eee0ee1e0\neee0e0e0000100\n0eeee00e1ee1e0\n000e0e001e11ee\n0ee001ee110011\ne0e01111e10111\n00e0e000001000\n0e0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 65.32249244000002, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee110011\n0ee01111e10111\n00e0e000001000\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 70.78252748, '00e00e000e0000\ne00e00e0e0eeee\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee110011\n0ee01111e10111\n00e0e000001000\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 70.78252748, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n0e0ee00e1ee1e0\n000e0e001e11ee\neee001ee110011\n00e01111e10111\n00e0e000001000\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 70.16194056, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee10e\neeee0e001e11ee\n00e001ee110011\n0ee01111e10111\n00e0e000001000\nee0e0e11e11101\ne00e00011e1e10\ne00eee0e1ee110\neee11111e11e11': 72.0641664, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\neeeee00e1ee1e0\n000e0e001e11ee\n0ee001ee110011\n0ee01111e10111\neee0e000001000\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 65.94407936, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n000ee00e1ee1e0\n0e0e0e001e11ee\neee001ee110011\n00e01111e10111\n00e0e000001000\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 69.41776872, '00e00e000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n000ee00e1ee1e0\n0eee0e001e11ee\n0ee001ee110011\ne0e01111e10111\n00e0e000001000\n0e0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 66.68825120000001}, {'00ee000eeee000\ne00e0e0ee0eee0\ne0e0eeeee0000e\nee000eee0ee1e0\neee0e0e0000100\n0eeee00e1ee1e0\n000e0e001e11ee\n0ee001ee110011\ne0e01111e10111\n00e0e000001000\n0e0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 63.95873368000001, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n0e0ee00e1ee1e0\n000e0e001e11ee\neee001ee110011\neee01111e10111\neee0e000001000\ne00e0e11e111e1\ne00e00011e1e1e\nee0eee0e1ee11e\neee11111e11e11': 63.253940760000006, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n000ee00e1ee1e0\n0eee0e001e11ee\n0ee001ee110011\ne0e01111e10111\n00e0e000001000\n0e0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 63.97319332000001, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee10e\neeee0e001e11ee\n00e001ee110011\n0ee01111e10111\n00e0e000001000\nee0e0e11e11101\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 68.75762188, '00e00e000e0000\ne00e00e0e0eeee\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee110011\n0ee01111e10111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 65.46931424, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee110011\n0ee01111e10111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 65.46931424, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee110011\ne0e01111e10111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 65.46931424, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n000ee00e1ee1e0\n0e0e0e001e11ee\neee001ee110011\n00e01111e10111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 64.10455548, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n0e0ee00e1ee1e0\n000e0e001e11ee\neee001ee110011\n00e01111e10111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 64.84872732000001, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\neeeee00e1ee1e0\n000e0e001e11ee\n0ee001ee110011\n0ee01111e10111\neee0e000001000\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 63.22902148000001}, {'00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n0e0ee00e1ee1e0\n000e0e001e11ee\neee001ee110011\neee01111e10111\neee0e000001eee\ne00e0e11e111e1\ne00e00011e1e1e\nee0eee0e1ee11e\neee11111e11e11': 57.94072752, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee110011\ne0e01111e10111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 60.02673884000001, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee10e\neeee0e001e11ee\n00e001ee110011\n0ee01111e10111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 59.949396240000006, '00eeee000e0000\ne00eeee0e0eeee\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee110011\n0ee01111e10111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 60.02673884000001, '00ee000eeee000\ne00e0e0ee0eee0\ne0e0eeeee0000e\nee000eee0ee1e0\neee0e0e0000100\n0eeee00e1ee1e0\n000e0e001e11ee\n0ee001ee110011\ne0e01111e10111\n00e0e000001eee\n0e0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 58.64552044, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n000ee00e1ee1e0\n0eee0e001e11ee\n0ee001ee110011\ne0e01111e10111\n00e0e000001eee\n0e0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 58.659980080000004, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee110011\n0ee01111e10111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 60.02673884000001, '00e00e000ee000\ne00e00e0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\neeeee00e1ee1e0\n000e0e001e11ee\n0ee001ee110011\n0ee01111e10111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 57.915808240000004, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n000ee00e1ee1e0\n0e0e0e001e11ee\neee001ee110011\n00e01111e10111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 58.66198008, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n0e0ee00e1ee1e0\n000e0e001e11ee\neee001ee110011\n00e01111e10111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 59.40615192}, {'00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee11ee11\n0ee01111e1e111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 53.23764156000001, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee11ee11\ne0e01111e1e111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 53.23764156000001, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n0e0ee00e1ee1e0\n000e0e001e11ee\neee001ee11ee11\n00e01111e1e111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 52.61705464, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n000ee00e1ee1e0\n0e0e0e001e11ee\neee001ee110011\neee01111e10111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 52.50015212, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\neeeee00e1ee1e0\n000e0e001e11ee\n0ee001ee110011\n0ee01111e10111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 52.47323284000001, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee10e\neeee0e001e11ee\n00e001ee11ee11\n0ee01111e1e111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 53.16029896, '00ee000eeee000\ne00e0e0ee0eee0\ne0e0eeeee0000e\nee000eee0ee1e0\neee0e0e0000100\n0eeee00e1ee1e0\n000e0e001e11ee\n0ee001ee110011\neee01111e10111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 52.4587732, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n000ee00e1ee1e0\n0eee0e001e11ee\n0ee001ee110011\neee01111e10111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 52.47323284000001, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n0e0ee00e1ee1e0\n000e0e001e11ee\neee001ee110011\neee01111e10111\neee0e000001eee\ne00e0e11e111e1\ne00e00011e1e1e\nee0eee0e1ee11e\neee11111e11e11': 52.49815212000001, '00eeee000e0000\ne00eeee0e0eeee\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee11ee11\n0ee01111e1e111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 53.23764156000001}, {'00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n0e0ee00e1ee1e0\n000e0e001e11ee\neee001ee11ee11\n00e01111e1e111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 45.711054839999996, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee11ee11\ne0e01111e1e111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 46.33164176000001, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n000ee00e1ee1e0\n0e0e0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 45.711054839999996, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n000ee00e1ee1e0\n0eee0e001e11ee\n0ee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 45.68413556, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee1e0\neeee0e001e11ee\n00e001ee11ee11\n0ee01111e1e111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 46.36764176000001, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n0e0ee00e1ee1e0\n000e0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\ne00e0e11e111e1\ne00e00011e1e1e\nee0eee0e1ee11e\neee11111e11e11': 45.70905484, '00ee000eeee000\ne00e0e0ee0eee0\ne0e0eeeee0000e\nee000eee0ee1e0\neee0e0e0000100\n0eeee00e1ee1e0\n000e0e001e11ee\n0ee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 45.669675919999996, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\n0e000eee0ee1e0\n0ee0e0e0000100\n000ee00e1ee10e\neeee0e001e11ee\n00e001ee11ee11\n0ee01111e1e111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 46.25429916, '00eeee000ee000\ne00eeee0e0eee0\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\neeeee00e1ee1e0\n000e0e001e11ee\n0ee001ee11ee11\n0ee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 45.68413556}, {'00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n000ee00e1ee1e0\n0eee0e001e11ee\n0ee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 38.778135760000005, '00ee000eeeeeee\ne00e0e0ee0eeee\ne0e0eeeee0000e\nee000eee0ee1e0\neee0e0e0000100\n0eeee00e1ee1e0\n000e0e001e11ee\n0ee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 38.76367612, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n000ee00e1ee1e0\n0e0e0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 38.80505504, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\neeeee00e1ee1e0\neeee0e001e11ee\n00e001ee11ee11\ne0e01111e1e111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 38.806055040000004, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\neeeee00e1ee1e0\neeee0e001e11ee\n00e001ee11ee11\n0ee01111e1e111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 38.842055040000005, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n0e0ee00e1ee1e0\n000e0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\ne00e0e11e111e1\ne00e00011e1e1e\nee0eee0e1ee11e\neee11111e11e11': 38.803055040000004, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\n0e0ee00e1ee1e0\n000e0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 38.80505504, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\neeeee00e1ee1e0\n000e0e001e11ee\n0ee001ee11ee11\n0ee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 38.778135760000005, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1e0\neee0e0e0000100\neeeee00e1ee10e\neeee0e001e11ee\n00e001ee11ee11\n0ee01111e1e111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 38.728712439999995}, {'00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\n000e0e001e11ee\n0ee001ee11ee11\n0ee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 30.497513800000004, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1ee\neee0e0e00001ee\n000ee00e1ee1ee\n0eee0e001e11ee\n0ee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 30.497513800000004, '00ee000eeeeeee\ne00e0e0ee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\n0eeee00e1ee1ee\n000e0e001e11ee\n0ee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 30.483054160000002, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1ee\neee0e0e00001ee\n000ee00e1ee1ee\n0e0e0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 30.52443308, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\n00e001ee11ee11\ne0e01111e1e111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 30.525433080000003, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\n00e001ee11ee11\n0ee01111e1e111\n00e0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 30.596433080000004, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1ee\neee0e0e00001ee\n0e0ee00e1ee1ee\n000e0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\ne00e0e11e111e1\ne00e00011e1e1e\nee0eee0e1ee11e\neee11111e11e11': 30.522433080000003, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1ee\neee0e0e00001ee\n0e0ee00e1ee1ee\n000e0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 30.52443308}, {'00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\ne00e0e11e111e1\ne00e00011e1e1e\nee0eee0e1ee11e\neee11111e11e11': -48.48787636, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': -48.241876360000006, '00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\n0eeee00e1ee1ee\n000e0e001e11ee\n0ee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111ee\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 21.547338, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111ee\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': 21.820257280000007, '00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\n0eeee00e1ee1ee\n000e0e001e11ee\n0ee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111e1\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': -48.33719116, '00eeee000eeeee\ne00eeee0e0eeee\ne0e0eee0e0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\ne00e0e11e111ee\ne00e00011e1e1e\nee0eee0e1ee11e\neee11111e11e11': 21.57425728}, {'00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\ne00e0e11e111ee\ne00e00011e1e1e\nee0eee0e1ee11e\neee11111eeee11': 11.897825679999999, '00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\ne00e0e11e111ee\ne00e00011e1e1e\nee0eee0e1ee11e\neee11111e11e11': -42.19392672, '00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111ee\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111e11e11': -41.916926720000006, '00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0e000001eee\nee0e0e11e111ee\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111eeee11': 12.174825679999998}, {'00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0eeeeee1eee\nee0e0e11e111ee\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111eeee11': -34.2767306, '00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11ee11\neee01111e1e111\neee0eeeeee1eee\ne00e0e11e111ee\ne00e00011e1e1e\nee0eee0e1ee11e\neee11111eeee11': -34.553730599999994, '00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11eeee\neee01111e1eeee\neee0eeeeee1eee\ne00e0e11e111ee\ne00e00011e1e1e\nee0eee0e1ee11e\neee11111eeee11': 3.55310196, '00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11eeee\neee01111e1eeee\neee0eeeeee1eee\nee0e0e11e111ee\ne00e00011e1e1e\ne00eee0e1ee11e\neee11111eeee11': 3.8301019600000004}, {'00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11eeee\neee01111e1eeee\neee0eeeeee1eee\neeee0e11e111ee\neeee00011e1e1e\neeeeee0e1ee11e\neeeeeeeeeeee11': 1.7611233600000005, '00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11eeee\neee01111e1eeee\neee0eeeeee1eee\neeee0e11e111ee\neeee00011e1e1e\neeeeee0e1ee11e\neee11111eeee11': -30.424599079999993}, {'00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11eeee\neee01111e1eeee\neee0eeeeee1eee\neeeeee11e111ee\neeeeeee11e1e1e\neeeeeeee1ee11e\neeeeeeeeeeee11': -27.99254935999999, '00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeee0e001e11ee\neee001ee11eeee\neee01111e1eeee\neee0eeeeee1eee\neeeeeeeee111ee\neeeeeeeeee1e1e\neeeeeeeeeee11e\neeeeeeeeeeee11': -1.3034554000000012}, {'00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeeeee001e11ee\neeeee1ee11eeee\neeee1111e1eeee\neeeeeeeeee1eee\neeeeeeeee111ee\neeeeeeeeee1e1e\neeeeeeeeeee11e\neeeeeeeeeeee11': -24.416765439999995, '00eeeeeeeeeeee\ne00eeeeee0eeee\ne0e0eeeee0000e\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeeeee001e11ee\neeeeeeee11eeee\neeeeeeeee1eeee\neeeeeeeeee1eee\neeeeeeeee111ee\neeeeeeeeee1e1e\neeeeeeeeeee11e\neeeeeeeeeeee11': -5.00908396}, {'00eeeeeeeeeeee\ne00eeeeeeeeeee\ne0e0eeeeeeeeee\nee000eee0ee1ee\neee0e0e00001ee\neeeee00e1ee1ee\neeeeee001e11ee\neeeeeeee11eeee\neeeeeeeee1eeee\neeeeeeeeee1eee\neeeeeeeee111ee\neeeeeeeeee1e1e\neeeeeeeeeee11e\neeeeeeeeeeee11': -21.599197759999992, '00eeeeeeeeeeee\ne00eeeeeeeeeee\ne0e0eeeeeeeeee\nee000eee0eeeee\neee0e0e0000eee\neeeee00e1eeeee\neeeeee001eeeee\neeeeeeee11eeee\neeeeeeeee1eeee\neeeeeeeeee1eee\neeeeeeeee111ee\neeeeeeeeee1e1e\neeeeeeeeeee11e\neeeeeeeeeeee11': -6.839266119999998}, {}, {}, {}]

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
            if str(newgameState.getBoard()) in self.gameStateValue[leftnum - 1].keys():
                if self.gameStateValue[leftnum - 1][str(newgameState.getBoard())] > max:
                    bestaction = action
                    max = self.gameStateValue[leftnum - 1][str(newgameState.getBoard())]
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
