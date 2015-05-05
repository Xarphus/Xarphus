#!/usr/bin/env python
# -*- coding:utf-8 -*-

FILE_NAME = "MDI_Window.py"

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
    from src.example import MyCustomDialog
    from src.ui_pp_update import Update_Window
except:
    print "Error"

class MDI_Window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.ui = os.path.abspath(os.path.join("gui", 'pp_mdi.ui'))

        try:
            self.ui = QUiLoader()
            self.file.open(QFile.ReadOnly)
            self.myWidget = self.ui.load(file, self)
            self.file.close()
            print "STATUS [OK]  ", FILE_NAME
            print "STATUS [MESSAGE]  (", FILE_NAME,  "): GUI is loaded from PySide"
        except:
            self.ui_mdi = loadUi(self.ui, self)
            print "STATUS [OK]  ", FILE_NAME
            print "STATUS [MESSAGE]  (", FILE_NAME,  "): GUI is loaded from PyQt4"


        # call the function
        self.set_mdiArea()
        self.set_actions_menubar()

    def set_actions_menubar(self):
        self.ui_mdi.actionOnUpdate.triggered.connect(self.create_update_form)

    def set_mdiArea(self):
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.mdiArea.setOption(QMdiArea.DontMaximizeSubWindowOnActivation, True)
        self.setCentralWidget(self.mdiArea)

    def create_update_form(self):
        # open example from here
        from src.example import MyCustomDialog
        self.example_dialog = MyCustomDialog()
        self.example_dialog.show()

        # you can open my update_form
#        from src.ui_pp_update import Update_Window
#        self.update_form = Update_Window()
#        self.update_form.show_and_raise()

    def show_and_raise(self):
        self.show()
        self.raise_()

    def closeEvent(self, event):
        sys.exit()

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

window = MDI_Window()
window.show_and_raise()

sys.exit(app.exec_())
