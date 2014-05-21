# -*- coding: utf-8 -*-
# AI agents

from game import printNotDefined

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
                    return self.evaluationFunction(gameState)

                v = 99999
                for move in gameState.getLegalActions(agentIndex):
                    v = min(alphabeta(depth, gameState.generateSuccessor(agentIndex,move), 1 - agentIndex, alpha, beta), v)
                    if v <= alpha:
                        return v
                    beta = min(beta,v)
                return v

        tmp = alphabeta(1, gameState, self.index, -99999, 99999)
        print "action:",tmp
        return tmp

    def evaluationFunction(self, gameState):
        return gameState.getScores(self.index) - gameState.getScores(1 - self.index) + len(gameState.getLegalActions(self.index)) - len(gameState.getLegalActions(1 - self.index))

defaultAgent = stupidAgent
abAgent = AlphaBetaAgent
srAgent = stupidReverseAgent

from learn import extractFeatures, FEATURES, evalFunc

class ReflexLinearAgent(Agent):
    def __init__(self, index, evalFunc = evalFunc):
        Agent.__init__(self, index)

        self.weights = (0.8910675658865255, -3.1839751011649087, -0.2879020903914638, -1.0871294643958471, 2.469392715066099)#(0.4034291420404963, -1.974784328730528, -0.7064027925005527, -1.6819318793652704, 1.207184735264548)
        self.evalFunc = evalFunc

    def setWeight(self, weights):
        self.weights = tuple(weights)

    def getAction(self, gameState):
        return max(gameState.getLegalActions(self.index), key = lambda action: self.evalFunc(gameState.generateSuccessor(self.index, action), self.index, self.weights))


rlAgent = ReflexLinearAgent
