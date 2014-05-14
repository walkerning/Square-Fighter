# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

ITEM_PICS = [':item%d'%x for x in range(21)]

ITEM_INI_ROINDEX = []

class Ui_TabWidget(QTabWidget):
    def __init__(self, parent = None):
        QTabWidget.__init__(self, parent)

        self.setFocusPolicy(Qt.NoFocus)
        widget0 = SquareListWidget(range(4))
        widget1 = SquareListWidget(range(4, 9))
        widget2 = SquareListWidget(range(9, 21))
        self.widgets = [widget0, widget1, widget2]

        self.addTab(widget0, "<= 3")
        self.addTab(widget1, "4")
        self.addTab(widget2, "5")
        for widget in self.widgets:
            #print widget.metaObject().indexOfSignal("itemPressed")
            #self.connect(widget, SIGNAL("currentItemChanged(QListWidgetItem*,QListWidgetItem*)"), self.on_currentItemChanged)
            self.connect(widget, SIGNAL("itemSelectionChanged()"), self.on_currentItemChanged)

    def on_currentItemChanged(self):
        pileIndex = self.sender().currentItem().data(SquareListWidget.PILE_INDEX_ROLE).toInt()
        self.emit(SIGNAL("currentPileChanged"), pileIndex[0])

    def removePile(self, pileIndex):
        if pileIndex < 4:
            self.widgets[0].removePile(pileIndex)
        elif pileIndex < 9:
            self.widgets[1].removePile(pileIndex)
        else:
            self.widgets[2].removePile(pileIndex)

    def resetPiles(self):
        #for widget in self.widgets:
        #del widget
        self.clear()
        widget0 = SquareListWidget(range(4))
        widget1 = SquareListWidget(range(4, 9))
        widget2 = SquareListWidget(range(9, 21))
        self.widgets = [widget0, widget1, widget2]

        self.addTab(widget0, "<= 3")
        self.addTab(widget1, "4")
        self.addTab(widget2, "5")
        for widget in self.widgets:
            self.connect(widget, SIGNAL("itemSelectionChanged()"), self.on_currentItemChanged)




    def setSelectionMode(self, mode):
        if mode == 1:
            for widget in self.widgets:
                widget.setSelectionMode(QAbstractItemView.SingleSelection)
        elif mode == 0:
            for widget in self.widgets:
                widget.setSelectionMode(QAbstractItemView.NoSelection)

class SquareListWidget(QListWidget):
    PILE_INDEX_ROLE = 32
    #ROTATE_INDEX_ROLE = 33
    def __init__(self, _list, parent = None):
        QListWidget.__init__(self, parent)

        #self.setViewMode(QListWidget.IconMode)

        self.itemDict = {}
        for i in _list:
            item = QListWidgetItem(QIcon(QPixmap(ITEM_PICS[i])), QString("pile%d"%i),self)
            item.setData(self.PILE_INDEX_ROLE, i)
            self.itemDict[i] = item
            #item.setData(ROTATE_INDEX_ROLE, ITEM_INI_ROINDEX[i])

    def removePile(self, pileIndex):
        item =  self.removeItemWidget(self.itemDict[pileIndex])
        del item
