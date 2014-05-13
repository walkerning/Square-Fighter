# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

ITEM_PICS = [[':item%d0'%x for x in range(21)],
             [':item%d1'%x for x in range(21)]]
ITEM_INI_ROINDEX = []

class Ui_TabWidget(QTabWidget):
    currentPileChanged = pyqtSignal(int)
    def __init__(self, player, parent = None):
        QTabWidget.__init__(self, parent)

        widget0 = SquareListWidget(range(4), player)
        widget1 = SquareListWidget(range(4, 9), player)
        widget2 = SquareListWidget(range(9, 21), player)
        self.widgets = [widget0, widget1, widget2]

        self.addTab(self, widget0, "<= 3")
        self.addTab(self, widget1, "4")
        self.addTab(self, widget2, "5")
        for widget in self.widgets:
            self.connect(widget, SIGNAL("currentItemChanged(QListWidgetItem,QListWidgetItem)"), self.on_currentItemChanged)

    def on_currentItemChanged(self, A, B):
        pileIndex = B.data(SquareListWidget.PILE_INDEX_ROLE).toInt()
        self.currentPileChanged.emit(pileIndex)

class SquareListWidget(QListWidget):
    PILE_INDEX_ROLE = 32
    #ROTATE_INDEX_ROLE = 33
    def __init__(self, _list, player, parent = None):
        QListWidget.__init__(self, parent)

        self.setViewMode(QListWidget.IconMode)

        for i in _list:
            item = QListWidgetItem(QIcon(QPixmap(ITEM_PICS[player][i])), self)
            item.setData(PILE_INDEX_ROLE, i)
            #item.setData(ROTATE_INDEX_ROLE, ITEM_INI_ROINDEX[i])
