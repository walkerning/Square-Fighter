#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 游戏的图形界面

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import gameRunner
import AIagents
from ui.ui_aivsai import Ui_GameWindow
from UireplayWidget import ReplayWidget
from functools import partial
import cPickle


class GameThread(QThread, gameRunner.Game):
    def __init__(self, agents, parent = None):
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
        while not self.isFinished and not self.isStopped():
            action = self.agents[self.index].getAction(self.nowState)
            #self.generateSuccessor(self.agents[self.index].getAction(self.nowState))
            #print "index:", self.index,"action:", action
            self.generateSuccessor(action)

        if not self.isStopped():
            self.settlement()
            self.emit(SIGNAL("gameFinished"), self.recordList)

class GameRunnerGui(QWidget, Ui_GameWindow):
    """
    Gui game runner.
    """
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

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
        self.connect(self.replayButton, SIGNAL("clicked()"), self.replayGame)
        self.connect(self.pauseButton, SIGNAL("toggled(bool)"), self.replayWidget, SLOT("Pause(bool)"))
        self.connect(self.debugCheck, SIGNAL("toggled(bool)"), self.replayWidget, SLOT("setShowDebug(bool)"))
        self.connect(self.nextRoundButton, SIGNAL("clicked()"), self.replayWidget.NextRound)

    def startGame(self):
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

        self.gameThread = GameThread(agentList)
        self.connect(self.gameThread, SIGNAL("gameFinished"), self.on_gameFinished)
        self.connect(self.gameThread, SIGNAL("finished()"), self.gameThread, SLOT("deleteLater()"))
        self.endButton.setEnabled(True)
        self.saveRecordButton.setEnabled(False)
        self.replayButton.setEnabled(False)
        self.gameThread.start()

    def endGame(self):
        if self.gameThread.isRunning():
            self.gameThread.stop()
            self.gameThread.wait()
            self.gameThread.deleteLater()
        self.endButton.setEnabled(False)
        self.replayButton.setEnabled(True)

    def saveGame(self):
        self.saveRecordButton.setEnabled(False)
        import time
        filename = "%s-vs-%s"%tuple(self.agentList) + time.strftime('%m-%d-%H-%M-%S',time.localtime(time.time())) + ".rep"
        f = file(filename, 'w')
        cPickle.dump(self.replayWidget.recordList, f)
        f.close()

    def replayGame(self):
        self.saveRecordButton.setEnabled(False)
        filename = QFileDialog.getOpenFileName(self, QString.fromUtf8("载入回放文件"), ".", "replay files(*.rep)")
        if filename:
            f = open(filename)
            try:
                recordList = cPickle.load(f)
            except:
                QMessageBox.warning(self, QString.fromUtf8("Error"), QString.fromUtf8("回放文件读取错误，请确定回放文件正确"), QMessageBox.Ok, QMessageBox.NoButton)
                return
            finally:
                f.close()
            self.showResult(recordList[-1])
            self.replayWidget.loadRecord(recordList)
            self.replayWidget.Play(0)

    def showResult(self, result):
        if result[1] == -1:
            self.resultLabel.setText(QString.fromUtf8("平局"))
        else:
            self.resultLabel.setText(QString("agent%d Win"%(result[1] + 1)))
        self.leftSquareLabel1.setText("%d"%result[-1][0])
        self.leftSquareLabel2.setText("%d"%result[-1][1])

    def on_gameFinished(self, record):
        self.endButton.setEnabled(False)
        self.saveRecordButton.setEnabled(True)
        self.replayButton.setEnabled(True)
        self.showResult(record[-1])

        self.replayWidget.loadRecord(record)
        self.replayWidget.Play(0)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = GameRunnerGui()
    window.show()
    app.exec_()
