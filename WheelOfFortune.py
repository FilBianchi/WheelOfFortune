import sys
import os
import json
from PySide6.QtWidgets import QApplication
from utils import init_logging
from gui import MainWindow

'''Application entry point'''

if __name__ == "__main__":

    init_logging()

    app = QApplication(sys.argv)
    app.setOrganizationName("Fiaccomulata 2024")
    app.setApplicationName("Wheel Of Fortune")
    if getattr(sys, 'frozen', False):
        data_folder_path = sys._MEIPASS
    else:
        data_folder_path = os.path.dirname(
            os.path.abspath(sys.modules['__main__'].__file__)
        )
    with open(data_folder_path + '/version.json') as json_data:
        d = json.load(json_data)
        json_data.close()
        app.setApplicationVersion(d["FullSemVer"])
    main_window = MainWindow()

    main_window.show()
    app.exec()
