#!/usr/bin/env python
# -*- coding : utf-8 -*-
# 游戏的图形界面

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import squareFighter as SF
import agents
from functools import partial


class GameThread(QThread):
    def __init__(self, agents, parent = None):
        super(GameThread, self).__init__(parent)

        self.game = Game(agents)

    def run(self):
        self.game.startGame()
        self.emit(SIGNAL("gameFinished"), self.game.recordList)

class GameRunnerGui(QWidget, ui_aivsai.Ui_GameWindow):
    """
    Gui game runner.
    """
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.game = None

        # Gui initialize
        self.agentEdits = [self.agentEdit1, self.agentEdit2]
        self.replayWidget = ReplayWidget()
        self.gridWidgetLayout.addWidget(self.replayWidget)
        self.endButton.setEnabled(False)
        self.saveRecordButton.setEnabled(False)

        # button signal connections
        self.connect(self.startButton, SIGNAL("clicked()"), self.startGame)
        self.connect(self.saveRecordButton, SIGNAL("clicked()"), self.saveGame)
        self.connect(self.endButton, SIGNAL("clicked()"), self.endGame)

    def startGame(self):
        agents = reload(agents)
        agentList = []
        for agentEdit in self.agentEdits:
            agent = str(agentEdit.text)
            if not agent:
            agent = "defaultAgent"
            try:
                agentList.append(getattr(agents, agent))
            except:
                QMessageBox.warning(self, QString.fromUtf8("Error"), QString.fromUtf8("No %s in module agents.Default one used"%agent), QMessageBox.Ok, QMessageBox.NoButton)
                agentList.append(getattr(agents, "defaultAgent"))
                continue
            if not hasattr(agentList[-1], 'getAction'):
                QMessageBox.warning(self, QString.fromUtf8("Error"), QString.fromUtf8("%s seems not to be a legal agent with the getAction method!Default agent used."%agent), QMessageBox.Ok, QMessageBox.NoButton)
                agentList[-1] = getattr(agents, "defaultAgent")

        self.gameThread = GameThread(agentList)
        self.connect(self.gameThread, SIGNAL("gameFinished"), self.on_gameFinished)
        self.connect(self.gameThread, SIGNAL("finished()"), self.gameThread, SLOT("deleteLater()"))
        self.endButton.setEnabled(True)
        self.gameThread.start()

    def endGame(self):
        if self.gameThread.isRunning():
            self.gameThread.exit()
            self.gameThread.deleteLater()

    def on_gameFinished(self, record):
        self.endButton.setEnabled(False)
        self.replayWidget.loadRecord(record)
        self.replayWidget.Play(0, 0)
