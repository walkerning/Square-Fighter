#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 实现可以每方是由人操作还是由AI操作的界面

from gui import UiTabWidget
from UireplayWidget import ReplayWidgetWithHuman
from ui.humanai import Ui_GameWindow

PLAYERS = [0, 0]
WaitForAction = QWaitCondition()

class GameThread(QThread, gameRunner.Game):
    def __init__(self, agents, players, parent = None):
        QThread.__init__(self, parent)
        gameRunner.Game.__init__(self, agents, True)

        self.mutex = QMutex()
        self.__stop = False

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
        self.mutex.lock()
        while not self.isFinished and not self.isStopped():

            #self.generateSuccessor(self.agents[self.index].getAction(self.nowState))
            #print "index:", self.index,"action:", action
            if not self.players[self.index]:
                self.action = self.agents[self.index].getAction(self.nowState)
            else:
                self.emit(SIGNAL("humanAction(int)", self.index))
                WaitForAction.wait(self.mutex)
            self.generateSuccessor(self.action)
            self.emit(SIGNAL("recordRecv"), self.record[-1])

        if not self.isStopped():
            self.settlement()
            self.emit(SIGNAL("gameFinished()"))

class GameRunnerWithHuman(QWidget, Ui_GameWindow):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.replayWidget = ReplayWidgetWithHuman()
        self.saveRecordButton.setEnabled(False)
        self.endButton.setEnabled(False)

        self.players = [False, False]
        self.started = False
        self.pileListWidgets = [Ui_TabWidget(), Ui_TabWidget()]

        for _list in self.pileListWidgets:
            self.connect(_list, SIGNAL("currentPileChanged(int)"), self.on_currentPileChanged)
        self.connect(self.replayWidget, SIGNAL("actionMade"), self.on_actionMade)

        self.connect(self.startButton, SIGNAL("clicked()"), self.startGame)
        self.connect(self.endButton, SIGNAL("clicked()"), self.endGame)
        self.connect(self.saveRecordButton, SIGNAL("clicked()"), self.saveGame)


    def startGame(self):
        self.players[0] = self.playerCheck1.isChecked()
        self.players[1] = self.playerCheck2.isChecked()
        for i in range(len(self.pileListWidgets)):
            self.pileListWidgets[i].resetPiles()
            if self.players[i]:
                self.pileListWidgets[i].setSelectionMode(QAbstractItemView.SingleSelection)
            else:
                self.pileListWidgets[i].setSelectionMode(QAbstractItemView.NoSelection)
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

        self.gameThread = GameThread(agentList, self.players)
        self.connect(self.gameThread, SIGNAL("humanAction()"), self.replayWidget.beginAction)
        self.connect(self.gameThread, SIGNAL("gameFinished()"), self.on_gameFinished)
        self.connect(self.gameThread, SIGNAL("recordRecv"), self.on_recordRecv)
        self.connect(self.gameThread, SIGNAL("finished()"), self.gameThread, SLOT("deleteLater()"))

        self.replayWidget.startGame(self.players)
        self.startButton.setEnabled(False)
        self.endButton.setEnabled(True)

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
        filename = "%s-vs-%s"%tuple(self.agentList) + time.strftime('%m-%d-%H-%M-%S',time.localtime(time.time())) + ".rep"
        f = file(filename, 'w')
        cPickle.dump(self.replayWidget.recordList, f)
        f.close()

    def on_currentPileChanged(self, pileIndex):
        sender = self.sender()
        if not sender in self.pileListWidgets:
            return
        playerIndex = self.pileListWidgets.index(sender)
        if not self.players[playerIndex]:
            print "oh my god"
            return
        self.replayWidget.setCurrentPile(playerIndex, pileIndex)

    def on_recordRecv(self, record):
        self.replayWidget.recordList.append(record)
        self.replayWidget.GoToRound(len(record) - 1)
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
        self.showResult(record[-1])

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
