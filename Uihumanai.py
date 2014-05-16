#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 实现可以每方是由人操作还是由AI操作的界面

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from gui.UiTabWidget import Ui_TabWidget
from UireplayWidget import ReplayWidgetWithHuman
from ui.ui_humanai import Ui_GameWindow
import gameRunner
import AIagents
import cPickle

WaitForAction = QWaitCondition()

class GameThread(QThread, gameRunner.Game):
    recordRecv = pyqtSignal([tuple])
    def __init__(self, agents, players, func, parent = None):
        QThread.__init__(self, parent)
        gameRunner.Game.__init__(self, agents, True)

        self.mutex = QMutex()
        self.__stop = False
        self.action = None
        self.players = players
        self.func = func

    def stop(self):
        try:
            self.mutex.lock()
            self.__stop = True
        finally:
            self.mutex.unlock()

    def isStopped(self):
        try:
            self.mutex.lock()
            return self.__stop
        finally:
            self.mutex.unlock()

    def run(self):
        while not self.isFinished and not self.isStopped():
            if not self.players[self.index]:
                self.action = self.agents[self.index].getAction(self.nowState)
            else:
                self.emit(SIGNAL("humanAction(int)"), self.index)
                self.mutex.lock()
                WaitForAction.wait(self.mutex)
                self.mutex.unlock()
            if not self.isStopped():
                self.generateSuccessor(self.action)
                #self.recordRecv.emit(self.recordList[-1])
                self.emit(SIGNAL("recordRecv"), self.recordList[-1], self.index)
                #self.func(self.recordList[-1])
        if not self.isStopped():
            self.settlement()
            self.emit(SIGNAL("gameFinished"), self.recordList)

class GameRunnerWithHuman(QWidget, Ui_GameWindow):
    #class EventFilter(QEventFilter:
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.replayWidget = ReplayWidgetWithHuman()

        self.saveRecordButton.setEnabled(False)
        self.endButton.setEnabled(False)
        self.setFixedSize(self.size())

        self.players = [False, False]
        self.started = False
        self.pileListWidgets = [Ui_TabWidget(), Ui_TabWidget()]
        self.agentEdits = [self.agentEdit1, self.agentEdit2]

        self.gridWidgetLayout.addWidget(self.replayWidget)
        self.pileListLayout0.addWidget(self.pileListWidgets[0])
        self.pileListLayout1.addWidget(self.pileListWidgets[1])

        for _list in self.pileListWidgets:
            _list.setFocusPolicy(Qt.NoFocus)
            self.connect(_list, SIGNAL("currentPileChanged"), self.on_currentPileChanged)
        self.connect(self.replayWidget, SIGNAL("actionMade"), self.on_actionMade)

        self.connect(self.startButton, SIGNAL("clicked()"), self.startGame)
        self.connect(self.endButton, SIGNAL("clicked()"), self.endGame)
        self.connect(self.saveRecordButton, SIGNAL("clicked()"), self.saveGame)
        self.connect(self.debugCheck, SIGNAL("toggled(bool)"), self.replayWidget, SLOT("setShowDebug(bool)"))

    def startGame(self):
        self.players[0] = self.playerCheck1.isChecked()
        self.players[1] = self.playerCheck2.isChecked()
        for i in range(len(self.pileListWidgets)):
            self.pileListWidgets[i].resetPiles()
            if self.players[i]:
                self.pileListWidgets[i].setSelectionMode(1)
            else:
                self.pileListWidgets[i].setSelectionMode(0)

        self.resultLabel.setText("")
        self.leftSquareLabel1.setText("")
        self.leftSquareLabel2.setText("")
        reload(AIagents)

        agentList = []
        self.agentList = []
        for agentEdit in self.agentEdits:
            agent = str(agentEdit.text())
            if not agent:
                agent = "defaultAgent"
            if not hasattr(AIagents, agent) or not hasattr(getattr(AIagents, agent), 'getAction'):
                QMessageBox.warning(self, QString.fromUtf8("Error"), QString.fromUtf8("%s seems not to be a legal agent with the getAction method!Default agent used."%agent), QMessageBox.Ok, QMessageBox.NoButton)
                agent = "defaultAgent"
            self.agentList.append(agent)
            agentList.append(getattr(AIagents, agent)(self.agentEdits.index(agentEdit)))

        self.gameThread = GameThread(agentList, self.players, self.on_recordRecv)
        self.connect(self.gameThread, SIGNAL("humanAction(int)"), self.replayWidget.beginAction)
        self.connect(self.gameThread, SIGNAL("gameFinished"), self.on_gameFinished)
        self.connect(self.gameThread, SIGNAL("recordRecv"), self.on_recordRecv)

        #self.gameThread.recordRecv[tuple].connect(self.on_recordRecv, Qt.BlockingQueuedConnection)
        #self.gameThread.recordRecv[tuple].connect(self.on_recordRecv, Qt.DirectConnection)
        self.connect(self.gameThread, SIGNAL("finished()"), self.gameThread, SLOT("deleteLater()"))

        # for test;
        for _list in self.pileListWidgets:
            self.connect(_list, SIGNAL("currentPileChanged"), self.on_currentPileChanged)

        self.startButton.setEnabled(False)
        self.endButton.setEnabled(True)
        self.replayWidget.recordList = [tuple()]
        self.replayWidget.GoToRound(0)
        self.gameThread.start()

    def endGame(self):
        if self.gameThread.isRunning():
            self.gameThread.stop()
            WaitForAction.wakeAll()
            self.gameThread.wait()
            self.gameThread.deleteLater()

        self.endButton.setEnabled(False)
        self.startButton.setEnabled(True)

    def saveGame(self):
        self.saveRecordButton.setEnabled(False)
        import time
        nameList = self.agentList[:]
        for i in range(2):
            if self.players[i]:
                nameList[i] = 'human'
        filename = "%s-vs-%s"%tuple(nameList) + time.strftime('%m-%d-%H-%M-%S',time.localtime(time.time())) + ".rep"
        f = file(filename, 'w')
        cPickle.dump(self.replayWidget.recordList, f)
        f.close()

    def on_currentPileChanged(self, pileIndex):
        sender = self.sender()
        if not sender in self.pileListWidgets:
            return
        playerIndex = self.pileListWidgets.index(sender)
        if not self.players[playerIndex]:
            return
        self.replayWidget.setCurrentPile(playerIndex, pileIndex)

    def on_recordRecv(self, record, nextIndex):
        self.replayWidget.recordList.insert(-1, record)
        self.replayWidget.recordList[-1] = (nextIndex,)
        self.replayWidget.GoToRound(len(self.replayWidget.recordList) - 1)
        self.pileListWidgets[record[0]].removePile(record[1][0])

    def showResult(self, result):
        if result[1] == -1:
            self.resultLabel.setText(QString.fromUtf8("平局"))
        else:
            self.resultLabel.setText(QString("agent%d Win"%(result[1] + 1)))
        self.leftSquareLabel1.setText("%d"%result[-1][0])
        self.leftSquareLabel2.setText("%d"%result[-1][1])

    def on_gameFinished(self, recordList):
        self.saveRecordButton.setEnabled(True)
        self.endButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.replayWidget.recordList = recordList
        self.showResult(recordList[-1])
        self.replayWidget.releaseKeyboard()

    def on_actionMade(self, action):
        try:
            self.gameThread.mutex.lock()
            self.gameThread.action = action
            WaitForAction.wakeAll()
        finally:
            self.gameThread.mutex.unlock()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = GameRunnerWithHuman()
    window.show()
    app.exec_()
