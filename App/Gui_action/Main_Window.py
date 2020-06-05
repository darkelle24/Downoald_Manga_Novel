from PyQt5 import QtCore, QtGui, QtWidgets
from App.Gui.Main_Window import Ui_MainWindow
from App.Gui.MangaView import MangaView
from App.Gui.Flow_Layout import FlowLayout
from tools.Load.loadAllManga import loadAllManga

class Ui_MainWindow_Action(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.refresh()

    def refresh(self):
        self.mangas = loadAllManga("./manga")

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Resource/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.gridLayout = FlowLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")

        for manga in self.mangas:
            bt = MangaView(manga.name, "./Resource/nonbiri-nouka-193x278.png", manga.nbrChapterManga, parent=self.scrollAreaWidgetContents)
            self.gridLayout.addWidget(bt)

    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)