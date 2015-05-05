FILE_NAME = "del_after.py"
import os
import requests
import sys
import time



try:
    from PyQt4.QtCore import QThread, pyqtSignal, Qt, QSemaphore
    from PyQt4.QtGui import QVBoxLayout, QPushButton, QDialog, QProgressBar, QApplication, QMessageBox

    print "STATUS [OK]  ", FILE_NAME, ": All modules are imported from PyQt4"
except ImportError:
    from PyQt4.QtCore import QThread, pyqtSignal, Qt, QSemaphore
    from PyQt4.QtGui import QVBoxLayout, QPushButton, QDialog, QProgressBar, QApplication, QMessageBox

    print "STATUS [OK]  ", FILE_NAME, ": All modules are imported from PySide"


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

class Download_Thread(QThread):
    finished_thread = pyqtSignal()
    error_http = pyqtSignal()
    finished_download = pyqtSignal()
    notify_progress = pyqtSignal(int)

    def __init__(self, loc, link, parent=None):
        QThread.__init__(self, parent)

        self.url = link
        self.location = loc

        self._run_semaphore = QSemaphore(1)

    def run(self):
        print "log"
        try:
            time.sleep(0.5)
            print "Time is over"
            file = requests.get(self.url, stream=True)
            status = file.status_code
            re = file.reason
            print "re ", re
            print status
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
                    downloaded_bytes = fd.tell() # sehr genau und direkt
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
        #self.progressBarUpdate.setValue(0)
        #self.progressBarUpdate.setRange(0, 1)
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

        pushButtonCancel.clicked.connect(self.download_task.stop)
        self.set_progressbar()

    def on_start(self):
        self.progressBarUpdate.setRange(0, 0)
        self.download_task.start()

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

    def set_progressbar(self):
        self.progressBarUpdate.setStyleSheet(DEFAULT_STYLE)
 
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
        print "Close"
        self.progressBarUpdate.setValue(0)

    def closeEvent(self, event):
        self.download_task.stop()
 
def main():
    app = QApplication(sys.argv)
    window = MyCustomDialog()
    window.resize(600, 400)
    window.show
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
