from PyQt5 import QtCore, QtGui, QtWidgets
from App.Gui.Main_Window import Ui_MainWindow
from App.Gui.MangaView import MangaView
from App.Gui.Flow_Layout import FlowLayout

class Ui_MainWindow_Action(Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Resource/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.gridLayout = FlowLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")

        for i in range(20):
            bt = MangaView(f"Dab {i}", "./Resource/nonbiri-nouka-193x278.png", self.scrollAreaWidgetContents)
            self.gridLayout.addWidget(bt)

    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)