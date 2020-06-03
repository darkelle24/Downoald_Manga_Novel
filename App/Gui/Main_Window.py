# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\darke\Documents\GitHub\Downoald_Manga_Novel\App\Gui\Main_Window.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("c:\\Users\\darke\\Documents\\GitHub\\Downoald_Manga_Novel\\App\\Gui\\../../Resource/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFiles = QtWidgets.QMenu(self.menubar)
        self.menuFiles.setObjectName("menuFiles")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionChange_Directory = QtWidgets.QAction(MainWindow)
        self.actionChange_Directory.setObjectName("actionChange_Directory")
        self.actionAdd_new_manga = QtWidgets.QAction(MainWindow)
        self.actionAdd_new_manga.setObjectName("actionAdd_new_manga")
        self.actionRefresh = QtWidgets.QAction(MainWindow)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionOption = QtWidgets.QAction(MainWindow)
        self.actionOption.setObjectName("actionOption")
        self.actionAdd_new_update = QtWidgets.QAction(MainWindow)
        self.actionAdd_new_update.setObjectName("actionAdd_new_update")
        self.menuFiles.addAction(self.actionAdd_new_manga)
        self.menuFiles.addAction(self.actionAdd_new_update)
        self.menuFiles.addSeparator()
        self.menuFiles.addAction(self.actionChange_Directory)
        self.menuFiles.addAction(self.actionRefresh)
        self.menuFiles.addSeparator()
        self.menuFiles.addAction(self.actionOption)
        self.menuFiles.addAction(self.actionExit)
        self.menubar.addAction(self.menuFiles.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Download Manga Novel"))
        self.menuFiles.setTitle(_translate("MainWindow", "Files"))
        self.actionChange_Directory.setText(_translate("MainWindow", "Change directory"))
        self.actionChange_Directory.setStatusTip(_translate("MainWindow", "Change directory"))
        self.actionChange_Directory.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actionAdd_new_manga.setText(_translate("MainWindow", "Add new manga"))
        self.actionAdd_new_manga.setStatusTip(_translate("MainWindow", "Add new manga to the list with an URL"))
        self.actionAdd_new_manga.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionRefresh.setText(_translate("MainWindow", "Refresh"))
        self.actionRefresh.setStatusTip(_translate("MainWindow", "Refresh all the list (Mangas, Updates, Sites)"))
        self.actionRefresh.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Exit the software"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionOption.setText(_translate("MainWindow", "Option"))
        self.actionOption.setStatusTip(_translate("MainWindow", "Option"))
        self.actionOption.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionAdd_new_update.setText(_translate("MainWindow", "Add new update"))
        self.actionAdd_new_update.setStatusTip(_translate("MainWindow", "Add new update to the list with an URL"))
        self.actionAdd_new_update.setShortcut(_translate("MainWindow", "Ctrl+U"))
