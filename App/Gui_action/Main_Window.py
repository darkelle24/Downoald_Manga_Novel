from PyQt5 import QtCore, QtGui, QtWidgets
from App.Gui.Main_Window import Ui_MainWindow
from App.Gui.MangaView import MangaView, MangaFrame
from App.Gui.Flow_Layout import FlowLayout
from tools.Load.loadAllManga import loadAllManga
from tools.Command.Init import init
from include.Enum import MangaType
from App.Gui.PreciseMangaViewWidget import PreciseMangaView

class Ui_MainWindow_Action(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.sites, self.mangas, self.updates = init("./manga")

    def refreshMangaList(self):
        for i in reversed(range(self.gridLayout.count())):
            widget = self.gridLayout.takeAt(i).widget().deleteLater()
            if widget is not None:
                widget.setParent(None)
        if (self.MangaButton.isChecked()):
            self.initMangaList(MangaType.MANGA)
        elif (self.NovelButton.isChecked()):
            self.initMangaList(MangaType.NOVEL)

    def lambdaPreciseManga(self, manga):
        return lambda event : self.showPreciseManga(event, manga)

    def initMangaList(self, mangaType):
        self.mangas = loadAllManga("./manga")
        for idx, manga in enumerate(self.mangas):
            if ((mangaType == MangaType.MANGA and manga.nbrChapterManga != 0) or (mangaType == MangaType.NOVEL and manga.nbrChapterNovel != 0)):
                Form = MangaFrame(self.scrollAreaWidgetContents)
                Form.setObjectName("Test")
                bt = MangaView(manga, mangaType, parent=Form)
                bt.mouseReleaseEvent = self.lambdaPreciseManga(manga)
                self.gridLayout.addWidget(Form)

    def hideMangaList(self):
        self.scrollAreaWidgetContents.setVisible(False)

    def showMangaList(self):
        self.scrollAreaWidgetContents.setVisible(True)

    def showPreciseManga(self, event, manga):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            if event.button() == QtCore.Qt.LeftButton:
                self.hideMangaList()
                self.NovelButton.setEnabled(True)
                self.DownloadButton.setEnabled(True)
                self.NovelButton.setChecked(False)
                self.DownloadButton.setChecked(False)
                self.MangaButton.setChecked(False)
                self.MangaButton.setEnabled(True)
                self.preciseManga.manga = manga
                self.preciseManga.retranslateUi(self.preciseManga.PreciseMangaWidget)
                self.containerPreciseManga.setVisible(True)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Resource/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.MangaButton.toggled.connect(self.on_check_Manga)
        self.NovelButton.toggled.connect(self.on_check_Novel)
        self.MangaButton.setEnabled(False)
        self.DownloadButton.toggled.connect(self.on_check_Download)

        self.gridLayout = FlowLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")

        self.initMangaList(MangaType.MANGA)

        self.shortcutRefresh = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self.scrollAreaWidgetContents)
        self.shortcutRefresh.activated.connect(self.refreshMangaList)

        self.containerPreciseManga = QtWidgets.QFrame(self.Container)
        self.containerPreciseManga.setMinimumSize(QtCore.QSize(875, 550))

        if (len(self.mangas) != 0):
            self.preciseManga = PreciseMangaView(self.mangas[0], self.containerPreciseManga)
            self.preciseManga.setMinimumSize(QtCore.QSize(875, 550))
        self.containerPreciseManga.setVisible(False)

    def on_check_Manga(self,is_toggle):
        if is_toggle:
            self.containerPreciseManga.setVisible(False)
            self.showMangaList()
            self.NovelButton.setEnabled(True)
            self.DownloadButton.setEnabled(True)
            self.NovelButton.setChecked(False)
            self.DownloadButton.setChecked(False)
            self.refreshMangaList()
            self.MangaButton.setEnabled(False)

    def on_check_Novel(self,is_toggle):
        if is_toggle:
            self.containerPreciseManga.setVisible(False)
            self.showMangaList()
            self.MangaButton.setEnabled(True)
            self.DownloadButton.setEnabled(True)
            self.MangaButton.setChecked(False)
            self.DownloadButton.setChecked(False)
            self.refreshMangaList()
            self.NovelButton.setEnabled(False)

    def on_check_Download(self,is_toggle):
        if is_toggle:
            self.containerPreciseManga.setVisible(False)
            self.NovelButton.setEnabled(True)
            self.MangaButton.setEnabled(True)
            self.NovelButton.setChecked(False)
            self.MangaButton.setChecked(False)
            self.DownloadButton.setEnabled(False)
            self.hideMangaList()

    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)