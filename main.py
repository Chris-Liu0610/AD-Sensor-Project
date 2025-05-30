import os
import sys
sys.path.append('..')
sys.path.append('./app')

from PyQt6.QtWidgets import QApplication
from app.view.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())