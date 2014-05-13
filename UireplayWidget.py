# -*- coding: utf-8 -*-
# replay widget

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from functools import partial
import game

SIZE = 14
COLOR_LIST = [(255, 0, 0), (0, 0, 255), (255, 255, 255)]
DEBUG_COLOR_LIST = [(244, 164, 96, 120), (127, 255, 0, 90)]
UNIT_WIDTH = 30
EDGE_WIDTH = 2
ANI_TIME = 500


def GetPos(x, y):
    return QPointF(x * (UNIT_WIDTH + EDGE_WIDTH), y * (UNIT_WIDTH + EDGE_WIDTH))

class GridUnit(QGraphicsObject):
    def __init__(self, color = (255, 255, 255), parent = None):
        super(GridUnit, self).__init__(parent)

        self.color = color
        if color not in COLOR_LIST:
            self.setZValue(1)

    def boundingRect(self):
        return QRectF(0, 0, UNIT_WIDTH + EDGE_WIDTH, UNIT_WIDTH + EDGE_WIDTH)

    def setPos(self, x, y):
        QGraphicsObject.setPos(self, GetPos(x, y))
        self.position = (x, y)

    def setColor(self, color):
        self.color = color
        self.update()

    def paint(self, painter, option, widget = None):
        painter.save()

        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(*self.color))
        pen = QPen(QColor(220, 220, 220))
        pen.setWidth(2)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawRect(QRect(0, 0, UNIT_WIDTH + EDGE_WIDTH, UNIT_WIDTH + EDGE_WIDTH))

        painter.restore()

class RoundError(Exception):
    def __init__(self, value = ''):
        self.value = value
    def __str__(self):
        return self.value

class ReplayWidget(QGraphicsView):
    def __init__(self, parent = None):
        QTableWidget.__init__(self, parent)

        self.animation = None

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedSize(QSize((UNIT_WIDTH + EDGE_WIDTH) * (SIZE+1), (UNIT_WIDTH + EDGE_WIDTH) *(SIZE+1)))

        self.recordList = []
        self.unitList = []
        self.debugUnitList = []
        self.aniUnitList = []
        self.setScene(QGraphicsScene(self))

        self.isPaused = False
        self._showdebug = False
        self.connect(self, SIGNAL("nextRound(int)"), self, SLOT("Play(int)"))
        self.round = 0


    def loadRecord(self, record):
        self.recordList = record
        self.round = 0

    def _setInitialState(self, state):
        gridBoardData = state.data.boardData
        #print "setInitialState!"
        for i in range(gridBoardData.size):
            for j in range(gridBoardData.size):
                new_unit = GridUnit(COLOR_LIST[gridBoardData[i][j]])
                self.scene().addItem(new_unit)
                new_unit.setPos(i, j)
                self.unitList.append(new_unit)

    def _setState(self, state):
        gridBoardData = state.data.boardData
        for i in range(gridBoardData.size):
            for j in range(gridBoardData.size):
                unit = self.scene().items(GetPos(i, j))[-1]
                unit.setColor(COLOR_LIST[gridBoardData[i][j]])

    def _resetState(self):
        for unit in self.unitList:
            self.scene().removeItem(unit)
        self.unitList = []

    def _resetDebug(self):
        for unit in self.debugUnitList:
            self.scene().removeItem(unit)
        self.debugUnitList = []


    def GoToRound(self, roundn):
        self._TerminateAni()
        if not self.recordList:
            return
        if roundn > len(self.recordList) - 1 or roundn < 0:
            raise RoundError("no round %d exist"%roundn)
        #test
        self.round = roundn
        if roundn == 0:
            self._resetState()
            self._setInitialState(game.GameState())
        else:
            self._setState(self.recordList[roundn - 1][-1])
        self._resetDebug()
        if self._showdebug:
            self._ShowDebug()


    @pyqtSlot(bool)
    def Pause(self, value):
        self.isPaused = value
        self.Play(self.round)

    @pyqtSlot(bool)
    def setShowDebug(self, value):
        self._showdebug = value
        self._resetDebug()
        if value and self.recordList:
            self._ShowDebug()

    def _ShowDebug(self):
        self._resetDebug()
        if self.round == len(self.recordList) - 1:
            return
        if self.round == 0:
            state = game.GameState()
        else:
            state = self.recordList[self.round - 1][-1]
        availGrids, impoGrids = state._getAvailableAndImportantGrids(self.recordList[self.round][0])
        for pos in impoGrids:
            unit = GridUnit(DEBUG_COLOR_LIST[0])
            self.scene().addItem(unit)
            unit.setPos(pos[0], pos[1])
            self.debugUnitList.append(unit)
        for pos in availGrids:
            unit = GridUnit(DEBUG_COLOR_LIST[1])
            self.scene().addItem(unit)
            unit.setPos(pos[0], pos[1])
            self.debugUnitList.append(unit)

    def NextRound(self):
        self.emit(SIGNAL("nextRound(int)"), self.round + 1)

    @pyqtSlot(int)
    def Play(self, roundn):
        if not self.recordList:
            return
        try:
            self.GoToRound(roundn)
        except:
            return
        if roundn == len(self.recordList) - 1:
            return
        if self.isPaused:
            return
        (index, action, correct,_) = self.recordList[roundn]
        if not correct and not self.isPaused:
            self.emit(SIGNAL("nextRound(int)"), roundn + 1)
            return
        self.animation = self._PlaceAnimation(index, action)
        self.connect(self.animation, SIGNAL("finished()"), self.animation, SLOT("deleteLater()"))
        self.connect(self.animation, SIGNAL("finished()"), self._resetAni)
        if not self.isPaused:
            self.connect(self.animation, SIGNAL("finished()"), partial(self.Play, roundn + 1))
        self.animation.start()


    def _PlaceAnimation(self, index, action):
        color = COLOR_LIST[index]
        pileIndex, squarePos, rotateIndex = action
        localPosList = game.PileRotateList[pileIndex][rotateIndex]
        ani = QParallelAnimationGroup()

        for lpos in localPosList:
            unit = self.scene().items(GetPos(squarePos[0] + lpos[0], squarePos[1] + lpos[1]))[-1]
            unit.setColor(color)
            unit.setOpacity(0)
            self.aniUnitList.append(unit)
            tmp_ani = QPropertyAnimation(unit, "opacity")
            tmp_ani.setDuration(ANI_TIME)
            tmp_ani.setStartValue(0)
            tmp_ani.setKeyValueAt(0.3, 1)
            tmp_ani.setKeyValueAt(0.6, 0.2)
            tmp_ani.setKeyValueAt(1, 1)
            ani.addAnimation(tmp_ani)
        return ani

    def _TerminateAni(self):
        if self.animation:
            self.animation.stop()
            self.animation.deleteLater()
            self.animation = None
        self._resetAni()

    def _resetAni(self):
        for item in self.aniUnitList:
            item.setOpacity(1)
        self.aniUnitList = []


class ReplayWidgetWithHuman(ReplayWidget):

#for test:
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    replaywidget = ReplayWidget()
    replaywidget._setInitialState(game.GameState())
    replaywidget.show()
    app.exec_()
