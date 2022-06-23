import time
import psutil
import requests
from PySide2 import QtCore, QtWidgets
from ui import P3_HardwareIndependentIO_QThread_design


# class MyApp(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         self.initTreads()
#         self.initUi()
#
#
#     def initUi(self):
#         self.lineEdit = QtWidgets.QLineEdit()
#         self.lineEdit.setPlaceholderText('Введите количество секунд')
#
#         self.pbStart = QtWidgets.QPushButton()
#         self.pbStart.setText('старт')
#
#         self.pbStop = QtWidgets.QPushButton()
#         self.pbStop.setText('стоп')
#         self.pbStop.setEnabled(False)
#
#         main_layout = QtWidgets.QVBoxLayout()
#         main_layout.addWidget(self.lineEdit)
#         main_layout.addWidget(self.pbStart)
#         main_layout.addWidget(self.pbStop)
#
#         self.setLayout(main_layout)
#
#         self.pbStart.clicked.connect(self.onPBStartClicked)
#         self.pbStop.clicked.connect(self.onPBStopClicked)
#
#     def initTreads(self):
#         self.timerThread = TimerTread()
#
#         self.timerThread.started.connect(self.timerStarted)
#         self.timerThread.finished.connect(self.timerFinished)
#
#         self.timerThread.timerSignal.connect(self.timerSignalEmit)
#
#     def onPBStartClicked(self):
#         try:
#             self.timerThread.timercount = int(self.lineEdit.text())
#             self.timerThread.start()
#         except ValueError:
#             self.lineEdit.setText('')
#             QtWidgets.QMessageBox.warning(self, 'ошибка', 'введено неправильное значение')
#
#     def onPBStopClicked(self):
#         self.timerThread.status = False
#
#     def timerStarted(self):
#         self.pbStart.setEnabled(False)
#         self.pbStop.setEnabled(True)
#         self.lineEdit.setEnabled(False)
#
#     def timerFinished(self):
#         self.pbStart.setEnabled(True)
#         self.pbStop.setEnabled(False)
#         self.lineEdit.setEnabled(True)
#
#         self.lineEdit.setText('')
#
#     def timerSignalEmit(self, emit_value):
#         self.lineEdit.setText(emit_value)
#
#
# class TimerTread(QtCore.QThread):
#     timerSignal = QtCore.Signal(str)
#
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         self.timercount = None
#         self.status = True
#
#     def run(self):
#         self.status = True
#         while self.status:
#             time.sleep(1)
#             self.timercount -= 1
#             self.timerSignal.emit(str(self.timercount))
#         # for i in range(self.timercount, 0, -1):
#         #     self.timerSignal.emit(str(i))
#         #     time.sleep(1)

class MyApp(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = P3_HardwareIndependentIO_QThread_design.Ui_Form()
        self.ui.setupUi(self)

        self.timerThread = Timer()
        self.timerThread.timerSignal.connect(self.updateLineEditTimeLeft, QtCore.Qt.AutoConnection)
        self.timerThread.finished.connect(self.pbstop)

        self.urlTread = UrlChecked()
        self.urlTread.urlsignal.connect(self.updateUrlCheck, QtCore.Qt.AutoConnection)

        self.ui.pushButtonTimerStart.clicked.connect(self.pbstart)
        self.ui.pushButtonUrlCheckStart.clicked.connect(self.url_checker)

    def pbstart(self):
        if self.ui.pushButtonTimerStart.isChecked():
            self.ui.lineEditTimerEnd.setText(str(self.ui.spinBoxTimerCount.value()))
            self.timerThread.timercount = self.ui.spinBoxTimerCount.value()
            self.timerThread.start()
            self.ui.pushButtonTimerStart.setText("Стоп")
        else:
            self.pbstop()

    def pbstop(self):
        self.ui.pushButtonTimerStart.setText("Начать отсчёт")
        self.ui.pushButtonTimerStart.setChecked(False)
        self.timerThread.status = False

    def updateLineEditTimeLeft(self):
        self.ui.lineEditTimerEnd.setText(str(self.timerThread.timercount))

    def url_checker(self):
        self.urlTread.url = self.ui.lineEditURL.text()
        self.ui.spinBoxUrlCheckTime.value(self.urlTread.delay)
        self.urlTread.start()

    def updateUrlCheck(self, status_code):
        self.ui.plainTextEditUrlCheckLog.appendPlainText(f"{time.ctime()} - Статус {status_code}")

class Timer(QtCore.QThread):
    timerSignal = QtCore.Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.timercount = None
        self.status = True

    def run(self):
        self.status = True
        while self.status:
            if not self.timercount == 0:
                time.sleep(1)
                self.timercount -= 1
                self.timerSignal.emit(str(self.timercount))

            else:
                self.status = False


class UrlChecked(QtCore.QThread):
    urlsignal = QtCore.Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.url = None
        self.delay = None

    def run(self):
        self.status = True

        while self.status:
            responce = requests.get(self.url)
            self.urlsignal.emit(responce.status_code)
            time.sleep(self.delay)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    win = MyApp()
    win.show()

    app.exec_()