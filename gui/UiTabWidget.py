# -*- coding: utf-8 -*-

ITEM_PICS = [[':item%d0'%x for x in range(21)],
             [':item%d1'%x for x in range(21)]]
ITEM_INI_INDEX = []
ITEM_HOTSPOT = []

class Ui_TabWidget(QTabWidget):
    def __init__(self, player, parent = None):
        QTabWidget.__init__(self, parent)

        widget0 = SquareListWidget(range(4), player)
        widget1 = SquareListWidget(range(4, 9), player)
        widget2 = SquareListWidget(range(9, 21), player)

        self.addTab(self, widget0, "<= 3")
        self.addTab(self, widget1, "4")
        self.addTab(self, widget2, "5")


class SquareListWidget(QListWidget):
    def __init__(self, _list, player, parent = None):
        QListWidget.__init__(self, parent)

        self.setViewMode(QListWidget.IconMode)

        self.items = [QListWidgetItem(QIcon(QPixmap(ITEM_PICS[player][i])), QString(str(ITEM_INI_INDEX[i])), self) for i in _list]

        def startDrag(self, dropAction):
            item = self.currentItem()
            data = QByteArray()
            index = int(item.text())

            stream = QDataStream(data, QIODevice.WriteOnly)
            stream << QVariant(index)
            mimeData = QMimeData()
            mimeData.setData("app/squarePile", data)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(*ITEM_HOTSPOT[index]))
            drag.setPixmap(item.icon().pixmap())
            drag.start(Qt.MoveAction)
