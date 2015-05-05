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



class Update_Window(QDialog):

    # def __init__(self, parent=None):
    #     QDialog.__init__(self, parent)
    def __init__(self, parent=None):
        super(Update_Window, self).__init__(parent)

        self.getPath_update = os.path.abspath(os.path.join('gui', 'pp_update.ui'))

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


        # Set data for download and saving in path
        self.location = os.path.abspath(os.path.join('temp', 'example-app-0.3.win32.zip'))
        self.url = 'http://sophus.bplaced.net/download/example-app-0.3.win32.zip'

        self.download_task = Download_Thread(self.location, self.url)
        self.download_task.notify_progress.connect(self.on_progress)
        self.download_task.finished_thread.connect(self.on_finished)
        self.download_task.error_http.connect(self.on_HTTPError)
        self.download_task.finished_download.connect(self.on_finish_download)

        self.ui_pp_update.pushButtonUpdate.setEnabled(True)
        self.create_actions_buttons()

    def on_start(self):
        self.ui_pp_update.progressBarUpdate.setRange(0, 0)
        self.download_task.start()

    def on_finish_download(self):
        msg_box = QMessageBox()
        QMessageBox.question(msg_box, ' Message ',
                                           "The file has been fully downloaded.", msg_box.Ok)

    def on_HTTPError(self):
        reply = QMessageBox.question(self, ' Error ',
                                           "The file could not be downloaded. Will they do it again?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.on_start()
        else:
            event.ignore()

    def on_progress(self, i):
        self.ui_pp_update.progressBarUpdate.setRange(0, 100)
        self.ui_pp_update.progressBarUpdate.setValue(i)

    def stop_progress(self):
        self.download_task.stop()
        self.ui_pp_update.progressBarUpdate.setValue(0)

    def check_folder_exists(self):
        location = os.path.abspath(os.path.join('temp'))
        if not os.path.exists(location):
            os.makedirs(location)
            print "Folder was created"
            self.on_start()
        else:
            print "Folder already exists"
            self.on_start()

    def on_finished(self):
        self.download_task.stop()
        self.ui_pp_update.progressBarUpdate.setValue(0)
        self.close()

    def set_ui_pp_update(self):
        self.ui_pp_update.progressBarUpdate.setAlignment(Qt.AlignCenter)
        self.ui_pp_update.progressBarUpdate.setValue(0)

    def create_actions_buttons(self):
        self.ui_pp_update.pushButtonUpdate.clicked.connect(self.check_folder_exists)
        self.ui_pp_update.pushButtonCancel.clicked.connect(self.stop_progress)
        self.ui_pp_update.pushButtonClose.clicked.connect(self.on_finished)

    def closeEvent(self, event):
        self.download_task.stop()

    def show_and_raise(self):
        self.show()
        self.raise_()

class Download_Thread(QThread):
    finished_thread = pyqtSignal()
    error_http = pyqtSignal()
    finished_download = pyqtSignal()
    notify_progress = pyqtSignal(int)

    def __init__(self, loc, link):
        QThread.__init__(self)

        self.url = link
        self.location = loc

        self._run_semaphore = QSemaphore(1)

    def run(self):
        try:
            file = requests.get(self.url, stream=True)
            status = file.status_code
            re = file.reason

            if not status == 200:
                self.error_http.emit()

        except (requests.exceptions.URLRequired,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                requests.exceptions.Timeout,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout), g:
            print 'Could not download ', g
            #self.error_http.emit()
        else:
            file_size = int(requests.head(self.url).headers.get('content-length', [0]))
            print "%s Byte" %file_size
            result = file_size / (1024*5)
            print result
            chunk_size = int(result)
            downloaded_bytes = 0

            with open(self.location, 'wb') as fd:
                for chunk in file.iter_content(chunk_size):
                    fd.write(chunk)
                    downloaded_bytes = fd.tell() 
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Update_Window()
    window.show_and_raise()

    sys.exit(app.exec_())
