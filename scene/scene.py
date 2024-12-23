from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGraphicsScene, QGraphicsSimpleTextItem


class Scene(QGraphicsScene):

    def __init__(self):
        super().__init__()

        self.__title = ""
        self.__rows = []

        self.__selected_letters = []

        self.__title_item = None
        self.__rows_item = None

        # self.addItem(self.__rows)

    def set_phrase(self, phrase: str):
        rows = phrase.split("\n")
        self.__title = rows[0]
        self.__rows = rows[1:]

        if self.__title_item is not None:
            self.removeItem(self.__title_item)
        if self.__rows_item is not None:
            self.removeItem(self.__rows_item)

        self.__title_item = QGraphicsSimpleTextItem(self.__title)
        self.__title_item.setFont(QFont("Times", 30, QFont.Weight.ExtraBold, True))
        self.addItem(self.__title_item)
        self.__title_item.moveBy(0, 600)
        self.__rows_item = QGraphicsSimpleTextItem()
        self.__rows_item.setFont(QFont("Courier", 120, QFont.Weight.Bold))
        self.__rows_item.moveBy(-800, 0)
        self.addItem(self.__rows_item)

        self.reset()

    def reset(self):
        self.__selected_letters = []
        self.__update_text()

    def show_letter(self, letter: str) -> int:
        if letter.upper() in self.__selected_letters:
            return 0
        if not self.__search_letter(letter):
            return 1
        self.__selected_letters.append(letter.upper())
        self.__update_text()
        return 2

    def __update_text(self):
        rows = ""
        for row in self.__rows:
            for c in row:
                if (c != " ") and (c.upper() not in self.__selected_letters):
                    c = "-"
                rows += c.upper()
            rows += "\n"
        self.__rows_item.setText(rows)

    def __search_letter(self, f) -> bool:
        for row in self.__rows:
            for c in row:
                if c.upper() == f.upper():
                    return True
        return False
