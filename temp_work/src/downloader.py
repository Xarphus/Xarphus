FILE_NAME = "del_after.py"
import os
import requests
import sys

try:
    from PyQt4.QtCore import QThread, pyqtSignal, Qt, QSemaphore
    from PyQt4.QtGui import QVBoxLayout, QPushButton, QDialog, QProgressBar, QApplication, QMessageBox

    print "STATUS [OK]  ", FILE_NAME, ": All modules are imported from PyQt4"
except ImportError:
    from PyQt4.QtCore import QThread, pyqtSignal, Qt, QSemaphore
    from PyQt4.QtGui import QVBoxLayout, QPushButton, QDialog, QProgressBar, QApplication, QMessageBox

    print "STATUS [OK]  ", FILE_NAME, ": All modules are imported from PySide"

class Download_Thread(QThread):
    finished_thread = pyqtSignal()
    error_http = pyqtSignal()
    finished_download = pyqtSignal()
    notify_progress = pyqtSignal(int)

    def __init__(self, location, link, parent=None):
        QThread.__init__(self, parent)

        self.url = link
        self.location = location

        self._run_semaphore = QSemaphore(1)

    def run(self):
        try:
            file = requests.get(self.url, stream=True)
            status = file.status_code

            if not status == 200:
                self.error_http.emit()

        except (requests.exceptions.URLRequired,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                requests.exceptions.Timeout,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout), g:
            print 'Could not download ', g
            self.error_http.emit()
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

class MyCustomDialog(QDialog):
 
    def __init__(self):
        super(MyCustomDialog, self).__init__()
        layout = QVBoxLayout(self)
 
        # Create a progress bar and a button and add them to the main layout
        self.progressBarUpdate = QProgressBar(self)
        self.progressBarUpdate.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progressBarUpdate)

        pushButtonUpdate = QPushButton("Start", self)
        layout.addWidget(pushButtonUpdate)
        pushButtonCancel = QPushButton("Cancel", self)
        layout.addWidget(pushButtonCancel)
 
        pushButtonUpdate.clicked.connect(self.check_folder_exists)

        # Set data for download and saving in path
        self.location = os.path.abspath(os.path.join('temp', 'example-app-0.3.win32.zip'))
        self.url = 'http://sophus.bplaced.net/download/example-app-0.3.win32.zip'
 
        self.download_task = Download_Thread(self.location, self.url)
        self.download_task.notify_progress.connect(self.on_progress)
        self.download_task.finished_thread.connect(self.on_finished)
        self.download_task.error_http.connect(self.on_HTTPError)
        self.download_task.finished_download.connect(self.on_finish_download)

        pushButtonCancel.clicked.connect(self.on_finished)

    def on_start(self):
        self.progressBarUpdate.setRange(0, 0)
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
        self.progressBarUpdate.setRange(0, 100)
        self.progressBarUpdate.setValue(i)
 
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
        self.progressBarUpdate.setValue(0)
        self.close()

    def closeEvent(self, event):
        self.download_task.stop()
 
def main():
    app = QApplication(sys.argv)
    window = MyCustomDialog()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
