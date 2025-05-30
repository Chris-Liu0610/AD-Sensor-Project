from PyQt6.QtWidgets import (
    QComboBox,
    QDateEdit
)


class QDateEditNoWheel(QDateEdit):
    """
    A custom QDateEdit that disables the mouse wheel event to prevent date changes
    when scrolling the mouse wheel.
    """
    def wheelEvent(self, event):
        pass

class QComboBoxNoWheel(QComboBox):
    """
    A custom QComboBox that disables the mouse wheel event to prevent scrolling through options
    when using the mouse wheel.
    """
    def wheelEvent(self, event):
        pass