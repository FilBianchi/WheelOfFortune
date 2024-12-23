import logging
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QResizeEvent
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog, QInputDialog
from utils import ObjectLogger

from gui.spinthewheelwidget import SpinTheWheelWidget
from gui.ui_mainwindow import Ui_MainWindow
from scene import Scene


class MainWindow(QMainWindow, ObjectLogger, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.setWindowTitle(QApplication.instance().applicationName() +
                            " - " +
                            QApplication.instance().applicationVersion())

        self.__scene = Scene()
        self.graphicsView.setScene(self.__scene)

        self.actionOpen.triggered.connect(self.__open)
        self.resetPushButton.clicked.connect(self.__reset)
        self.showPushButton.clicked.connect(self.__show)
        self.spinPushButton.clicked.connect(self.__spin_the_wheel)
        self.addPushButton.clicked.connect(self.__add_row)

    def __open(self):
        filename, ext = QFileDialog.getOpenFileName(self, "Open", "Select file", "", "Phrases (*.phr)")
        print(filename, ext)
        if filename != "":
            f = open(filename, "r")
            s = f.read()
            f.close()
            self.__scene.set_phrase(s)
            self.graphicsView.fitInView(self.__scene.sceneRect())

    def __add_row(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())

    def __reset(self):
        self.__scene.reset()

    def __show(self):
        ll = QInputDialog.getText(self, "Show Letter", "Please insert a letter")
        if ll[1]:
            ret = self.__scene.show_letter(ll[0])
            if ret == 0:
                QMessageBox.warning(self, "Warning", "Already selected letter")
            elif ret == 1:
                QMessageBox.warning(self, "Warning", "Letter not found")

    def __spin_the_wheel(self):
        d = SpinTheWheelWidget()
        d.exec()
        print(d.result())

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.graphicsView.fitInView(self.__scene.sceneRect())

    def closeEvent(self, event: QCloseEvent) -> None:
        self._logger.debug("Close requested")
