# -*- coding: utf-8 -*-
# AI agents

class Agent:
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



defaultAgent = Agent
