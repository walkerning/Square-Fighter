#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 实现可以每方是由人操作还是由AI操作的界面

from gui import UiTabWidget
from ui.humanai import Ui_GameWindow

PLAYERS = [0, 0]

class GameRunnerWithHuman(QWidget, Ui_GameWindow):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.replayWidget = ReplayWidgetWithHuman()
