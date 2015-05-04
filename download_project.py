FILE_NAME = "ui_pp_update.py"

import os
import sys
import requests

try:
    from PyQt4.QtCore import QThread, Qt, pyqtSignal, QSemaphore
    from PyQt4.QtGui import QDialog, QIcon, QMessageBox, QApplication
    from PyQt4.uic import loadUi

    print "STATUS [OK]  ", FILE_NAME, ": All modules are imported from PyQt4"
except ImportError:
    from PySide.QtCore import QFile, QThread, Qt, pyqtSignal, QSemaphore
    from PySide.QtUiTools import QUiLoader
    from PySide.QtGui import QDialog, QIcon, QMessageBox, QApplication

    print "STATUS [OK]  ", FILE_NAME, ": All modules are imported from PySide"

try:
    from ..about.info import info_app
    from ..languages.german import Language
    print "STATUS [OK]  ", FILE_NAME, ": All modules are imported"
except IOError as (errno, strerror):
    print "STATUS [FAILED]  ", FILE_NAME, ": I/O error({0}): {1}".format(errno, strerror)
except ValueError as VE:
    print VE
    #print "STATUS [FAILED]  ", FILE_NAME, ": value error({0}): {1}".format(erno1, sterror1)
except:
    print "STATUS [FAILED]  ", FILE_NAME, ": Unexpected error:", sys.exc_info()[0]
    raise

MESSAGEBOX = """
QMessageBox {
    background: #222;
}
QMessageBox * {
    background: #222;
    color: #cccdcc;
}
QMessageBox QPushButton {
    width: 50px;
    height: 20px;
    background: #444;
    color: #aaa;
}
"""
DEFAULT_STYLE = """
QProgressBar{
    border: 1px solid grey;
    background-color: #E6E6E6;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: #498EEE;
    width: 10px;
    margin: 0px;
}"""


class Update_Window(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.getPath_update = os.path.abspath(os.path.join('files', "qt_ui", 'pp_update.ui'))
        self.set_language = Language()
        self.get_info = info_app()

        try:
            self.ui_pp_update = QUiLoader()
            self.file = QFile(self.getPath_search_ui, self)
            self.file.open(QFile.ReadOnly)
            self.myWidget = self.ui_pp_update.load(file, self)
            self.file.close()
            print "STATUS [OK]  ", FILE_NAME, ": GUI is loaded from PySide"
        except:
            self.ui_pp_update = loadUi(self.getPath_update, self)
            print "STATUS [OK]  ", FILE_NAME, ": GUI is loaded from PyQt4"

        self.ui_pp_update.setWindowModality(Qt.ApplicationModal)

        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.location = os.path.join(BASE_PATH, 'temp', 'example-app-0.3.win32.zip')

        self.url = 'http://sophus.bplaced.net/download/example-app-0.3.win32.zip'

        self.download_task = Download_Thread(self.location, self.url)
        self.download_task.notify_progress.connect(self.on_progress)
        self.download_task.finished_thread.connect(self.on_finished)
        self.download_task.error_http.connect(self.on_HTTPError)
        self.download_task.finished_download.connect(self.on_finish_download)

        self.set_progressbar()

        self.set_language_pp_ui_about()
        self.set_ui_pp_update()
        self.ui_pp_update.pushButtonUpdate.setEnabled(True)
        self.create_actions_buttons()
        self.set_progressbar()

    def on_download(self, i):
        self.progressBarUpdate.setValue(i)

    def on_start(self):
        self.progressBarUpdate.setRange(0, 0)
        self.download_task.start()

    def check_folder_exists(self):
        if not os.path.exists(self.location):
            os.makedirs(self.location)
            print "Folder was created"
            self.on_start()
        else:
            print "Folder already exists"
            self.on_start()

    def set_language_pp_ui_about(self):
        self.ui_pp_update.setWindowTitle(self.set_language.dict_ui_pp_update["pp_update_title"])
        self.ui_pp_update.pushButtonUpdate.setText(self.set_language.dict_ui_pp_update["pushButtonUpdate"])
        self.ui_pp_update.pushButtonCancel.setText(self.set_language.dict_ui_pp_update["pushButtonCancel"])
        self.ui_pp_update.pushButtonClose.setText(self.set_language.dict_ui_pp_update["pushButtonClose"])

    def create_actions_buttons(self):
        self.ui_pp_update.pushButtonUpdate.clicked.connect(self.check_folder_exists)
        self.ui_pp_update.pushButtonCancel.clicked.connect(self.download_task.stop)
        self.ui_pp_update.pushButtonClose.clicked.connect(self.on_finished)

    def set_progressbar(self):
        self.progressBarUpdate.setStyleSheet(DEFAULT_STYLE)

    def set_ui_pp_update(self):
        self.progressBarUpdate.setAlignment(Qt.AlignCenter)
        # self.progressBarUpdate.setRange(0, 0)
        self.progressBarUpdate.setValue(0)

    def on_finish_download(self):
        msh_box = QMessageBox()

        msh_box.setStyleSheet(MESSAGEBOX)
        QMessageBox.question(msh_box, ' Message ',
                                           "The file has been fully downloaded.", msh_box.Ok)

    def on_HTTPError(self):
        reply = QMessageBox.question(self, ' Error ',
                                           "The file could not be downloaded. Will they do it again?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.on_start()
        else:
            event.ignore()

    def on_progress(self, i):
        self.progressBarUpdate.setRange(0,100)
        self.progressBarUpdate.setValue(i)

    def on_finished(self):
        print "Close"
        self.progressBarUpdate.setValue(0)

    def closeEvent(self, event):
        self.download_task.stop()

class Download_Thread(QThread):
    finished_thread = pyqtSignal()
    error_http = pyqtSignal()
    finished_download = pyqtSignal()
    notify_progress = pyqtSignal(int)

    def __init__(self, location_downloaded_file, link_download):
        QThread.__init__(self)

        self.url_download = link_download
        self.location_file = location_downloaded_file

        self._run_semaphore = QSemaphore(1)

    def run(self):
        print "log", self.location_file
        print "url", self.url_download
        try:
            getfile = requests.get(self.url_download, stream=True)
            status1 = getfile.status_code
        except (requests.exceptions.URLRequired,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                requests.exceptions.Timeout,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout), g:
            print 'Could not download ', g
            self.error_http.emit()
        else:
            print "Los"
            file_size = int(requests.head(self.url_download).headers.get('content-length', [0]))
            print "%s Byte" %file_size
            result = file_size / (1024*5)
            print result
            chunk_size = int(result)
            downloaded_bytes = 0

            with open(self.location_file, 'wb') as fd:
                for chunk in getfile.iter_content(chunk_size):
                    fd.write(chunk)
                            #downloaded_bytes += chunk_size # zu ungenau
                    downloaded_bytes = fd.tell() # sehr genau und direkt
                            #downloaded_bytes += len(chunk) # auch nicht schlecht
                    print (float(downloaded_bytes)/file_size*100)
                    self.notify_progress.emit(float(downloaded_bytes)/file_size*100)

                    if self._run_semaphore.available() == 0:
                        self._run_semaphore.release(1)
                        break

                print "Finish"
                self.finished_download.emit()
                self.finished_thread.emit()

    def stop(self):
        print "stop"
        self._run_semaphore.acquire(1)
