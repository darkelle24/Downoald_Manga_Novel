from PyQt5 import QtCore, QtGui, QtWidgets
from App.Gui.Main_Window import Ui_MainWindow
from App.Gui.MangaView import MangaView, MangaFrame
from App.Gui.Flow_Layout import FlowLayout
from tools.Load.loadAllManga import loadAllManga
from tools.Command.Init import init
from include.Enum import MangaType

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

    def initMangaList(self, mangaType):
        self.mangas = loadAllManga("./manga")
        for manga in self.mangas:
            if ((mangaType == MangaType.MANGA and manga.nbrChapterManga != 0) or (mangaType == MangaType.NOVEL and manga.nbrChapterNovel != 0)):
                Form = MangaFrame(self.scrollAreaWidgetContents)
                Form.setObjectName("Test")
                if (mangaType == MangaType.MANGA):
                    bt = MangaView(manga.name, manga.pathImage, manga.nbrChapterManga, parent=Form)
                else:
                    bt = MangaView(manga.name, manga.pathImage, manga.nbrChapterNovel, parent=Form)
                self.gridLayout.addWidget(Form)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Resource/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.MangaButton.toggled.connect(self.on_check_Manga)
        self.NovelButton.toggled.connect(self.on_check_Novel)
        self.DownloadButton.toggled.connect(self.on_check_Download)

        self.gridLayout = FlowLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")

        self.initMangaList(MangaType.MANGA)

        self.shortcutRefresh = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self.scrollAreaWidgetContents)
        self.shortcutRefresh.activated.connect(self.refreshMangaList)

    def on_check_Manga(self,is_toggle):
        if is_toggle:
            self.NovelButton.setChecked(False)
            self.DownloadButton.setChecked(False)
            self.refreshMangaList()

    def on_check_Novel(self,is_toggle):
        if is_toggle:
            self.MangaButton.setChecked(False)
            self.DownloadButton.setChecked(False)
            self.refreshMangaList()

    def on_check_Download(self,is_toggle):
        if is_toggle:
            self.NovelButton.setChecked(False)
            self.MangaButton.setChecked(False)

    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)