#!/usr/bin/python3

from PyQt5 import QtCore, QtGui, QtWidgets
from App.Gui_action.Main_Window import Ui_MainWindow_Action

if (__name__== "__main__"):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_Action()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())