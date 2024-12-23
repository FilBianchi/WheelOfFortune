import abc
from typing import Optional

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget


class Device(QObject):
    opened = Signal()
    closed = Signal()
    error = Signal(str)

    def __init__(self):
        super().__init__()

    @property
    @abc.abstractmethod
    def description(self) -> str:
        pass

    @abc.abstractmethod
    def open(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass

    @abc.abstractmethod
    def is_opened(self) -> bool:
        pass

    @abc.abstractmethod
    def get_widget(self) -> Optional[QWidget]:
        pass

    @staticmethod
    @abc.abstractmethod
    def enumerate():
        pass
