#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The game runner

import game

class Game:
    """
    Game class encapsulate the rule of the square fighter game.
    """
    TIE = -1
    WIN0 = 0
    WIN1 = 1
    def __init__(self, agents):
        self.nowState = game.GameState()
        self.agents = agents
        self.canMove = [True, True]
        self.index = 0
        self.isFinished = False

    def reset(self):
        self.nowState = game.GameState()
        self.canMove = [True, True]
        self.index = 0
        self.isFinished = False

    def nextPlayer(self):
        for tmpIndex in [(self.index + i) % len(self.agents) for i in range(1, len(agents) + 1)]:
            tmpIndex = (self.index + 1) % len(self.agents)
            if self.canMove[tmpIndex] and self.nowState.getLegalActions(tmpIndex):
                self.index = tmpIndex
                return True
        return False

    def generateSuccessor(self, action):
        self.nowState = self.nowState.generateSuccessor(self.index, action)
        if not self.nextPlayer():
            self.isFinished = True

    def calculateSquare(self, pileIndexList):
        sqNum = 0
        for index in pileIndexList:
            sqNum += game.PileSquareNumberList[index]
        return sqNum

    def settlement(self):
        self.leftSquares = map(lambda index: calculateSquare(self.nowState.getLeftPiles(index)), [0, 1])
        minNum = min(self.leftSquares)
        self.winner = [x for x in [0, 1] if self.leftSquares[x] == minNum]
        if len(self.winner) == 2:
            self.result = Game.TIE
        else:
            self.result = self.winner[0]

def GameRunner(Game):
    """
    Non-Gui game runner.
    """
    def startGame(self):
        while not self.isFinished:
            self.generateSuccessor(self.index, self.agents[self.index].getAction(self.nowState))
        self.settlement()

# 解析命令行参数
def ParseArgument():
    pass

if __name__ == "__main__":
    # run game!
    pass
