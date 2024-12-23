import numpy
import sounddevice

from PySide6.QtCore import QTimer, QTimeLine, Signal, Qt
from PySide6.QtGui import QPixmap, QBrush
from PySide6.QtWidgets import QGraphicsScene, QGraphicsEllipseItem, QGraphicsPixmapItem, QGraphicsItemAnimation


class WheelScene(QGraphicsScene):
    loudness_change = Signal(int)

    loudness = 0

    def __init__(self):
        super().__init__()

        pixmap = QPixmap("wheel/wheel.png")
        self.__item = QGraphicsPixmapItem(pixmap)
        self.__item.setTransformOriginPoint(pixmap.width()/2, pixmap.height()/2)
        self.addItem(self.__item)
        circle = QGraphicsEllipseItem(pixmap.width()/2 - 50, 10, 100, 100)
        brush = QBrush()
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        circle.setBrush(brush)
        self.addItem(circle)

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__timeout)
        self.__timer.setInterval(50)
        self.__timer.start()
        self.__a = 0
        self.__speed = 0

        self.__stream = sounddevice.InputStream(callback=self.__audio_callback)
        self.__stream.start()

    def spin_the_wheel(self, **kwargs):
        if "force" in kwargs:
            if self.__speed < 0.5:
                self.__speed = 0.5
        else:
            self.__speed = WheelScene.loudness

    def brake(self):
        self.__speed *= 0.8

    @staticmethod
    def __audio_callback(indata, frames, time, status):
        WheelScene.loudness += numpy.sum(indata*indata)
        if WheelScene.loudness > 100:
            WheelScene.loudness = 100
        WheelScene.loudness *= 0.95

    def __timeout(self):
        self.loudness_change.emit(int(WheelScene.loudness))
        self.__item.setRotation(self.__a)
        self.__a += self.__speed
        if self.__speed > 0.2:
            self.__speed -= self.__speed * 0.04
        else:
            self.__speed = 0
