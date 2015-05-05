#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ---------
# IMPORT
# ---------
import sys
import os

try:
    from PyQt4.QtCore import QSize, Qt, SIGNAL
    from PyQt4.QtGui import QApplication, QMainWindow, QWorkspace, QAction, QMenu, QSystemTrayIcon, QIcon, QMessageBox, \
        QPushButton, QPixmap, QMdiArea, QToolButton, QToolBar, QMdiArea, QMdiSubWindow, QWidget, QBrush, QColor, QSplashScreen, \
        QProgressBar
    from PyQt4.uic import loadUi

    print "STATUS [OK]  ", FILE_NAME
    print "STATUS [MESSAGE]  (", FILE_NAME, "): All modules are imported from PyQt4"
except ImportError:
    from PySide.QtCore import QFile, QSize, Qt, SIGNAL
    from PySide.QtUiTools import QUiLoader
    from PySide.QtGui import QApplication, QMainWindow, QWorkspace, QAction, QMenu, QSystemTrayIcon, QIcon, QMessageBox, \
        QPushButton, QPixmap, QMdiArea, QToolButton, QToolBar, QMdiArea, QMdiSubWindow, QWidget, QBrush, QColor, QSplashScreen, \
        QProgressBar

# import own modules
try:
    from files.modules_ui.example import MyCustomDialog
    from files.modules_ui.ui_pp_update import Update_Window
except:
    print "Error"
# ---------
# DEFINE
#---------
class Mdi_Main(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        #--------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------
        self.getPath_mdi = os.path.abspath(os.path.join('files', "qt_ui", 'pp_mdi.ui'))
        print str(self.getPath_mdi)
        self.getPath_mdi1 = os.path.abspath(os.path.join('files', "qt_ui"))
        #--------------------------------------------------------------------------------------
        try:
            self.ui_pp_mdi = QUiLoader()
            self.file = QFile(self.getPath_search_ui, self)
            self.file.open(QFile.ReadOnly)
            self.myWidget = self.ui_pp_mdi.load(file, self)
            self.file.close()
            print "STATUS [OK]  ", FILE_NAME
            print "STATUS [MESSAGE]  (", FILE_NAME,  "): GUI is loaded from PySide"
        except:
            self.ui_pp_mdi = loadUi(self.getPath_mdi, self)
            print "STATUS [OK]  ", FILE_NAME
            print "STATUS [MESSAGE]  (", FILE_NAME,  "): GUI is loaded from PyQt4"
        #--------------------------------------------------------------------------------------

        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.mdiArea.setOption(QMdiArea.DontMaximizeSubWindowOnActivation, True)
        self.setCentralWidget(self.mdiArea)
        self.set_actions_menubar()
        #--------------------------------------------------------------------------------------
    def set_actions_menubar(self):
        #--------------------------------------------------------------------------------------
        self.ui_pp_mdi.actionOnUpdate.triggered.connect(self.create_update_form)
    #--------------------------------------------------------------------------------------
    def create_update_form(self):
        # open example from here
        from files.modules_ui.example import MyCustomDialog
        self.MyExampleDialog = MyCustomDialog()
        self.MyExampleDialog.show()

        # you can open my update_form
        from files.modules_ui.ui_pp_update import Update_Window
        self.MyUpdate = Update_Window()
        self.MyUpdate.show_and_raise()

    def show_and_raise(self):
        self.show()
        self.raise_()

#---------
# MAIN
#---------

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

window = Mdi_Main()
window.show_and_raise()

sys.exit(app.exec_())
