from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDateEdit


class QDateEditNoWheel(QDateEdit):
    """
    A custom QDateEdit that disables the mouse wheel event to prevent date changes
    when scrolling the mouse wheel.
    """
    def wheelEvent(self, event):
        pass

        