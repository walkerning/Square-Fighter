# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aivsai.ui'
#
# Created by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_GameWindow(object):
    def setupUi(self, GameWindow):
        GameWindow.setObjectName(_fromUtf8("GameWindow"))
        GameWindow.resize(778, 609)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GameWindow.sizePolicy().hasHeightForWidth())
        GameWindow.setSizePolicy(sizePolicy)
        GameWindow.setWindowOpacity(1.0)
        self.verticalLayoutWidget = QtGui.QWidget(GameWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(80, 20, 571, 471))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.gridWidgetLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.gridWidgetLayout.setMargin(0)
        self.gridWidgetLayout.setObjectName(_fromUtf8("gridWidgetLayout"))
        self.startButton = QtGui.QPushButton(GameWindow)
        self.startButton.setGeometry(QtCore.QRect(310, 520, 50, 50))
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.saveRecordButton = QtGui.QPushButton(GameWindow)
        self.saveRecordButton.setGeometry(QtCore.QRect(420, 520, 80, 50))
        self.saveRecordButton.setObjectName(_fromUtf8("saveRecordButton"))
        self.label = QtGui.QLabel(GameWindow)
        self.label.setGeometry(QtCore.QRect(70, 500, 81, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(GameWindow)
        self.label_2.setGeometry(QtCore.QRect(200, 500, 81, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.endButton = QtGui.QPushButton(GameWindow)
        self.endButton.setGeometry(QtCore.QRect(360, 520, 50, 50))
        self.endButton.setObjectName(_fromUtf8("endButton"))
        self.agentEdit1 = QtGui.QLineEdit(GameWindow)
        self.agentEdit1.setGeometry(QtCore.QRect(50, 530, 113, 20))
        self.agentEdit1.setAlignment(QtCore.Qt.AlignCenter)
        self.agentEdit1.setObjectName(_fromUtf8("agentEdit1"))
        self.agentEdit2 = QtGui.QLineEdit(GameWindow)
        self.agentEdit2.setGeometry(QtCore.QRect(190, 530, 113, 20))
        self.agentEdit2.setAlignment(QtCore.Qt.AlignCenter)
        self.agentEdit2.setObjectName(_fromUtf8("agentEdit2"))
        self.replayButton = QtGui.QPushButton(GameWindow)
        self.replayButton.setGeometry(QtCore.QRect(520, 520, 80, 50))
        self.replayButton.setObjectName(_fromUtf8("replayButton"))
        self.leftSquareLabel1 = QtGui.QLabel(GameWindow)
        self.leftSquareLabel1.setGeometry(QtCore.QRect(60, 570, 50, 25))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(116, 114, 112))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.leftSquareLabel1.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Adobe Courier"))
        font.setPointSize(12)
        self.leftSquareLabel1.setFont(font)
        self.leftSquareLabel1.setText(_fromUtf8(""))
        self.leftSquareLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.leftSquareLabel1.setObjectName(_fromUtf8("leftSquareLabel1"))
        self.leftSquareLabel2 = QtGui.QLabel(GameWindow)
        self.leftSquareLabel2.setGeometry(QtCore.QRect(240, 570, 50, 25))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(116, 114, 112))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.leftSquareLabel2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Adobe Courier"))
        font.setPointSize(12)
        self.leftSquareLabel2.setFont(font)
        self.leftSquareLabel2.setText(_fromUtf8(""))
        self.leftSquareLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.leftSquareLabel2.setObjectName(_fromUtf8("leftSquareLabel2"))
        self.resultLabel = QtGui.QLabel(GameWindow)
        self.resultLabel.setGeometry(QtCore.QRect(140, 560, 71, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(116, 114, 112))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.resultLabel.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Adobe Courier"))
        font.setPointSize(10)
        self.resultLabel.setFont(font)
        self.resultLabel.setText(_fromUtf8(""))
        self.resultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.resultLabel.setObjectName(_fromUtf8("resultLabel"))
        self.replayNameEdit = QtGui.QLineEdit(GameWindow)
        self.replayNameEdit.setGeometry(QtCore.QRect(610, 540, 131, 20))
        self.replayNameEdit.setReadOnly(True)
        self.replayNameEdit.setObjectName(_fromUtf8("replayNameEdit"))
        self.debugCheck = QtGui.QCheckBox(GameWindow)
        self.debugCheck.setGeometry(QtCore.QRect(670, 100, 92, 23))
        self.debugCheck.setObjectName(_fromUtf8("debugCheck"))
        self.pauseButton = QtGui.QPushButton(GameWindow)
        self.pauseButton.setGeometry(QtCore.QRect(720, 30, 51, 51))
        self.pauseButton.setCheckable(True)
        self.pauseButton.setObjectName(_fromUtf8("pauseButton"))
        self.nextRoundButton = QtGui.QPushButton(GameWindow)
        self.nextRoundButton.setGeometry(QtCore.QRect(660, 30, 51, 51))
        self.nextRoundButton.setObjectName(_fromUtf8("nextRoundButton"))

        self.retranslateUi(GameWindow)
        QtCore.QMetaObject.connectSlotsByName(GameWindow)

    def retranslateUi(self, GameWindow):
        GameWindow.setWindowTitle(_translate("GameWindow", "方格斗士", None))
        self.startButton.setText(_translate("GameWindow", "开始", None))
        self.saveRecordButton.setText(_translate("GameWindow", "保存至文件", None))
        self.label.setText(_translate("GameWindow", "agent1", None))
        self.label_2.setText(_translate("GameWindow", "agent2", None))
        self.endButton.setText(_translate("GameWindow", "终止", None))
        self.replayButton.setText(_translate("GameWindow", "播放回放", None))
        self.debugCheck.setText(_translate("GameWindow", "调试信息", None))
        self.pauseButton.setText(_translate("GameWindow", "暂停", None))
        self.nextRoundButton.setText(_translate("GameWindow", "下一回", None))

