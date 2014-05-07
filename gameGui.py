#!/usr/bin/env python
# -*- coding : utf-8 -*-
# 游戏的图形界面

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import squareFighter as SF
from functools import partial
"""
WaitForTurn=[QWaitCondition(), QWaitCondition()]

class AiThread(QThread):
    def __init__(self, agent, parent = None):
        super(AiThread, self).__init__(parent)

        self.mutex = QMutex()
        self.index = agent.index
        self.agent = agent
        self.gameState = None
        self.calculation = 0

    def stop(self):
        self.exit(0)

    def run(self):
        global WaitForTurn
        while True:
            self.mutex.lock()
            WaitForTurn[self.index].wait(self.mutex)
            self.calculation += 1
            self.emit(SIGNAL("commandRecv"), self.index, self.agent.getAction(self.gameState))
"""
class GameRunnerWithSignal(SF.Game):
    def startGame(self):
        while not self.isFinished:
            action = self.agents[self.index].getAction(self.nowState)
            self.emit(SIGNAL("commandRecv"), self.index, action)
            self.generateSuccessor(action)
        self.settlement()

class GameThread(QThread):
    def __init__(self, agents, parent = None):
        super(GameThread, self).__init__(parent)

        self.game = GameRunnerWithSignal(agents)

    def run(self):
        self.game.startGame()

class GameRunnerGui(QWidget, Game):
    """
    Gui game runner.
    """
    def __init__(self, agents, parent = None):
        QWidget.__init__(self, parent)
        Game.__init__(self, agents)
        self.setupUi(self)

        self.setFixedSize(self.size())
        self.replayWidget = ReplayWidget()
        self.gameThread = GameThread(agents)
        #self.aiThreads = [AiThread(agent, self) for agent in agents]

        # Gui initialization
        self.nextButton.setEnabled(False)

        # button signal connections
        self.connect(self.startButton, SIGNAL("clicked()"), self.startGame)
#        self.connect(self.endButton, SIGNAL("clicked()"), self.endGame)
        self.connect(self.pauseButton, SIGNAL("toggled(bool)"), self.pausePlay)
#        self.connect(self.nextButton, SIGNAL("clicked()"), partial(self.nextMove, 1))
#        self.connect(self.replayWidget, SIGNAL("replayFinished()"), partial(self.nextMove, 0))

        #for thread in self.aiThreads:
        self.connect(gameThread, SIGNAL("commandRecv"), self.on_commandRecv)

    def startGame(self):
        self.gameThread.start()

"""    def startGame(self):
        self.startButton.setEnabled(False)
        self.pauseButton.setEnabled(True)
        self.endButton.setEnabled(True)
        self.nextMove()

    def pauseGame(self, toggle):
        if toggle:
            self.nextButton.setEnabled(True)
        else:
            self.nextbutton.setEnabled(False)

    def nextMove(self, kind):
        if kind == 0 and self.isPaused: # replay finshed signal
            return
        if kind == 1:
            self.replayWidget.GoToRound()# 是先计算比较好把= =应该
        try:
            self.aiThreads[self.index].mutex.lock()
            self.aiThreads[self.index].gameState = self.nowState
        finally:
            self.aiThreads[self.index].mutex.unlock()
            WaitForTurn[self.index].wakeAll()

    def on_commandRecv(self, index, action):
        self.generateSuccessor(index, action)
        self.replayWidget.Play(index, action)

    def endGame(self):
        self.reset()
        self.startButton.setEnabled(True)
        self.pauseButton.setEnabled(False)
        self.endButton.setEnabled(False)
        self.nextButton.setEnabled(False)
"""
