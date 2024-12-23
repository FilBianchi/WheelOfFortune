from PySide6.QtGui import QResizeEvent, QShowEvent, QKeyEvent
from PySide6.QtWidgets import QDialog

from gui.ui_spinthewheelwidget import Ui_SpinTheWheelDialog
from wheel import WheelScene


class SpinTheWheelWidget(Ui_SpinTheWheelDialog, QDialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.__scene = WheelScene()
        self.graphicsView.setScene(self.__scene)

        self.spinPushButton.clicked.connect(self.__spin_the_wheel)
        self.__scene.loudness_change.connect(self.progressBar.setValue)

    def keyPressEvent(self, arg__1: QKeyEvent) -> None:
        if arg__1.key() == 65:
            self.__scene.spin_the_wheel(force=0.5)
        elif arg__1.key() == 90:
            self.__scene.brake()

    def showEvent(self, arg__1: QShowEvent) -> None:
        self.graphicsView.fitInView(0, 0, 4167, 4167)

    def resizeEvent(self, arg__1: QResizeEvent) -> None:
        self.graphicsView.fitInView(0, 0, 4167, 4167)

    def __spin_the_wheel(self):
        self.__scene.spin_the_wheel()

    def result(self):
        return 100

