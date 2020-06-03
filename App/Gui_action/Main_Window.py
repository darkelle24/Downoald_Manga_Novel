from PyQt5 import QtCore, QtGui, QtWidgets
from App.Gui.Main_Window import Ui_MainWindow

class Ui_MainWindow_Action(Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Resource/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)